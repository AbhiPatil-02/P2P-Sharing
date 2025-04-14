import os
import time
from typing import Optional, Tuple
from config import config
from utils import format_bytes, calculate_speed, safe_filename

def send_file(conn, filepath: str, progress_callback=None) -> Tuple[bool, str]:
    """Enhanced file transfer with detailed progress reporting"""
    try:
        filename = safe_filename(os.path.basename(filepath))
        if not os.path.exists(filepath):
            return (False, f"❌ File not found: {filename}")

        start_time = time.time()
        total_size = os.path.getsize(filepath)

        conn.send(filename.encode())
        ack = conn.recv(config.BUFFER_SIZE).decode().strip()
        if ack != "ACK":
            return (False, "❌ Connection handshake failed")

        sent_bytes = 0
        last_update = time.time()

        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(config.BUFFER_SIZE)
                if not chunk:
                    break
                try:
                    conn.send(chunk)
                    sent_bytes += len(chunk)

                    current_time = time.time()
                    if progress_callback and (current_time - last_update > 0.1 or len(chunk) > config.BUFFER_SIZE / 2):
                        progress_callback(sent_bytes, total_size)
                        last_update = current_time

                except ConnectionError as e:
                    return (False, f"❌ Connection lost during transfer: {str(e)}")

        if progress_callback:
            progress_callback(sent_bytes, total_size)
        conn.send(b"<EOF>")

        transfer_time = time.time() - start_time
        speed = calculate_speed(total_size, transfer_time)
        return (True, f"✅ {filename} ({format_bytes(total_size)}) sent in {transfer_time:.2f}s ({speed})")

    except Exception as e:
        return (False, f"❌ Error sending file: {str(e)}")

def receive_file(conn) -> Tuple[bool, Optional[str], str]:
    """Enhanced file reception with validation"""
    try:
        filename = safe_filename(conn.recv(config.BUFFER_SIZE).decode().strip())
        if not filename:
            return (False, None, "❌ Empty filename received")

        conn.send(b"ACK")
        save_path = os.path.join(config.SHARED_FOLDER, filename)
        temp_path = save_path + ".part"

        start_time = time.time()
        received_bytes = 0

        with open(temp_path, 'wb') as f:
            while True:
                data = conn.recv(config.BUFFER_SIZE)
                if not data:
                    return (False, None, "❌ Connection closed unexpectedly")

                if data.endswith(b"<EOF>"):
                    f.write(data[:-5])
                    received_bytes += len(data) - 5
                    break

                f.write(data)
                received_bytes += len(data)

        os.rename(temp_path, save_path)
        transfer_time = time.time() - start_time
        file_size = os.path.getsize(save_path)
        speed = calculate_speed(file_size, transfer_time)

        return (True, save_path, f"📥 Received {filename} ({format_bytes(file_size)}) in {transfer_time:.2f}s ({speed})")

    except Exception as e:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        return (False, None, f"❌ Error receiving file: {str(e)}")

def receive_loop(conn, callback=None):
    """Continuous file reception loop with enhanced logging"""
    while True:
        try:
            success, filepath, message = receive_file(conn)
            if not success:
                if "Connection closed" in message:
                    break
                if callback:
                    callback(f"⚠️ {message}")
                continue

            if callback:
                callback(filepath)
                callback(f"✨ {message}")

        except (ConnectionError, BrokenPipeError):
            if callback:
                callback("🔌 Connection closed by peer")
            break
        except Exception as e:
            if callback:
                callback(f"⚠️ Unexpected error: {str(e)}")
            break
