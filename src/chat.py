import socket
import threading
import json
import time
from typing import Callable, Optional
from config import config
from utils import encrypt_message, decrypt_message, format_timestamp
from animation import show_chat_notification

class ChatError(Exception):
    """Custom exception for chat-related errors"""
    pass

class ChatHandler:
    def __init__(self, is_server: bool, peer_ip: Optional[str], 
                 on_message_callback: Callable[[str], None],
                 encryption_key: Optional[str] = None):
        self.on_message_callback = on_message_callback
        self.encryption_key = encryption_key
        self.peer_ip = peer_ip
        self.is_server = is_server
        self.connection_established = False
        self.message_queue = []
        self.conn = None
        self.running = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(config.SOCKET_TIMEOUT)

        self._setup_connection()

        if self.connection_established:
            self.running = True
            threading.Thread(target=self._listen_loop, daemon=True).start()
            threading.Thread(target=self._process_queue, daemon=True).start()

    def _setup_connection(self):
        """Establish chat connection with retry logic"""
        max_attempts = 3 if self.is_server else config.MAX_RETRIES

        for attempt in range(1, max_attempts + 1):
            try:
                if self.is_server:
                    self._start_server()
                else:
                    self._connect_to_server()

                self.connection_established = True
                show_chat_notification("💬 Chat connected successfully!")
                return

            except (socket.timeout, ConnectionRefusedError) as e:
                show_chat_notification(f"⚠️ Chat error: {str(e)} (attempt {attempt}/{max_attempts})")
                if attempt < max_attempts:
                    time.sleep(config.RETRY_DELAY)

        show_chat_notification("💥 Failed to establish chat connection")

    def _start_server(self):
        self.sock.bind(('', config.CHAT_PORT))
        self.sock.listen(1)
        show_chat_notification("👂 Waiting for chat connection...")
        self.conn, addr = self.sock.accept()
        self.peer_ip = addr[0]
        self.conn.settimeout(config.SOCKET_TIMEOUT)

    def _connect_to_server(self):
        if not self.peer_ip:
            raise ChatError("No peer IP provided for client mode")
        show_chat_notification(f"🔗 Connecting to chat at {self.peer_ip}...")
        self.sock.connect((self.peer_ip, config.CHAT_PORT))
        self.conn = self.sock

    def _listen_loop(self):
        buffer = ""
        while self.running:
            try:
                data = self.conn.recv(config.BUFFER_SIZE).decode()
                if not data:
                    break

                buffer += data

                while "\n" in buffer:
                    msg, buffer = buffer.split("\n", 1)
                    self._process_incoming_message(msg)

            except socket.timeout:
                continue
            except Exception as e:
                show_chat_notification(f"⚠️ Chat error: {str(e)}")
                break

        self._handle_disconnect()

    def _process_incoming_message(self, raw_msg: str):
        try:
            msg_data = json.loads(raw_msg)
            text = msg_data.get('text', '')
            timestamp = msg_data.get('timestamp', '')

            if self.encryption_key:
                text = decrypt_message(text, self.encryption_key)

            display_msg = f"{format_timestamp(float(timestamp))} Peer: {text}"
            self._append_chat(display_msg, msg_type="remote")
            show_chat_notification("✉️ New message received")

        except json.JSONDecodeError:
            self._append_chat(f"Peer: {raw_msg}", msg_type="remote")
        except Exception as e:
            show_chat_notification(f"⚠️ Failed to process message: {str(e)}")

    def send(self, msg: str):
        if not msg.strip():
            return

        if not self.connection_established:
            self.message_queue.append(msg)
            return

        try:
            msg_data = {
                'text': encrypt_message(msg, self.encryption_key) if self.encryption_key else msg,
                'timestamp': time.time(),
                'sender': 'local'
            }
            formatted_msg = json.dumps(msg_data) + "\n"
            self.conn.send(formatted_msg.encode())
            show_chat_notification("📤 Message sent")
            self._append_chat(f"You: {msg}", msg_type="local")

        except Exception as e:
            show_chat_notification(f"⚠️ Failed to send message: {str(e)}")
            self.message_queue.append(msg)

    def _process_queue(self):
        while self.running:
            if self.connection_established and self.message_queue:
                msg = self.message_queue.pop(0)
                self.send(msg)
            time.sleep(0.5)

    def _handle_disconnect(self):
        show_chat_notification("🔌 Chat disconnected")
        self.running = False
        self.connection_established = False
        self.close()

    def close(self):
        self.running = False
        try:
            if self.conn:
                self.conn.close()
            self.sock.close()
        except Exception as e:
            show_chat_notification(f"⚠️ Error closing chat: {str(e)}")

    def _append_chat(self, msg: str, msg_type: str = "default"):
        colors = {
            "system": ("#27ae60", "#ffffff"),
            "error": ("#e74c3c", "#ffffff"),
            "local": ("#3498db", "#ffffff"),
            "remote": ("#9b59b6", "#ffffff"),
            "default": ("#2c3e50", "#ffffff")
        }

        fg, _ = colors.get(msg_type, colors["default"])
        r, g, b = int(fg[1:3], 16), int(fg[3:5], 16), int(fg[5:], 16)
        print(f"\033[38;2;{r};{g};{b}m{msg}\033[0m")
        if self.on_message_callback:
            self.on_message_callback(msg)
