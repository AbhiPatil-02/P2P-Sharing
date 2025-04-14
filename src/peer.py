import socket
import time
from typing import Optional
from config import config
from utils import get_local_ip
from animation import show_connection_animation

class PeerConnectionError(Exception):
    """Custom exception for peer connection issues"""
    pass

# Modified display_network_status with ANSI colors
def display_network_status(message, status="info"):
    colors = {
        "info": '34',     # Blue
        "success": '32',  # Green
        "error": '31',    # Red
        "warning": '33'   # Yellow
    }
    color_code = colors.get(status, '37')  # Default to white
    print(f"\033[1;{color_code}m{message}\033[0m", flush=True)

def start_server() -> socket.socket:
    """Start a listening server and accept a connection"""
    server_socket = None
    conn = None
    try:
        display_network_status("🔄 Starting server...", "info")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.settimeout(config.SOCKET_TIMEOUT)
        
        try:
            server_socket.bind(('', config.PORT))
        except OSError as e:
            raise PeerConnectionError(f"❌ Port {config.PORT} is already in use") from e
            
        server_socket.listen(1)
        local_ip = get_local_ip()
        display_network_status(f"👂 Listening on {local_ip}:{config.PORT}...", "success")
        show_connection_animation("Waiting for connection")
        
        try:
            conn, addr = server_socket.accept()
            display_network_status(f"✅ Connected by {addr[0]}", "success")
            show_connection_animation(f"Connection established with {addr[0]}")
            return conn
        except socket.timeout:
            raise PeerConnectionError("⌛ Connection timed out")

    except Exception as e:
        display_network_status(f"❌ Server error: {str(e)}", "error")
        raise PeerConnectionError(f"Server failed: {str(e)}") from e
    finally:
        if server_socket and conn is None:
            server_socket.close()

def connect_to_peer(ip: str) -> Optional[socket.socket]:
    """Connect to a peer with retry logic"""
    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            display_network_status(f"🔗 Connecting to {ip} (attempt {attempt}/{config.MAX_RETRIES})...", "info")
            show_connection_animation(f"Connecting to {ip}")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(config.SOCKET_TIMEOUT)
            sock.connect((ip, config.PORT))
            
            display_network_status(f"✅ Successfully connected to {ip}", "success")
            show_connection_animation(f"Connected to {ip}")
            return sock
            
        except (socket.timeout, ConnectionRefusedError, socket.error) as e:
            display_network_status(f"⚠️ Attempt {attempt} failed: {str(e)}", "warning")
            if attempt < config.MAX_RETRIES:
                time.sleep(config.RETRY_DELAY)
    
    display_network_status(f"💥 Failed to connect to {ip} after {config.MAX_RETRIES} attempts", "error")
    return None

def verify_connection(conn: socket.socket) -> bool:
    """Verify if the connection is still active"""
    try:
        conn.send(b'')
        return True
    except socket.error:
        return False
