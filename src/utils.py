import os
import socket
import platform
import time
import base64
import json
import hashlib
import random
from datetime import datetime
from typing import Optional, Tuple, Dict, Any, List, Callable
from pathlib import Path
from cryptography.fernet import Fernet

# ======================
# NETWORK UTILITIES
# ======================

def is_valid_ip(ip: str) -> bool:
    """Validate IPv4 or IPv6 address"""
    try:
        if ':' in ip:  # IPv6
            socket.inet_pton(socket.AF_INET6, ip)
        else:  # IPv4
            socket.inet_pton(socket.AF_INET, ip)
        return True
    except (socket.error, ValueError):
        return False

def get_local_ip() -> str:
    """Get the machine's local IP address that others can connect to"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.error:
            return "127.0.0.1"

def get_network_info() -> Dict[str, Any]:
    """Get comprehensive network information about the current machine"""
    return {
        "hostname": socket.gethostname(),
        "local_ip": get_local_ip(),
        "is_online": check_internet_connection(),
        "platform": platform.platform(),
        "timestamp": datetime.now().isoformat()
    }

def display_network_status(message: str) -> None:
    """Display formatted network status message with emoji indicator"""
    print(f"🌐 {message}", flush=True)

def check_internet_connection(timeout: float = 3.0) -> bool:
    """Check if the machine has an active internet connection"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False

def get_available_port(start_port: int = 5000, end_port: int = 6000) -> Optional[int]:
    """Find an available network port in the given range"""
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except socket.error:
                continue
    return None

# ======================
# FILE UTILITIES
# ======================

def get_file_hash(filepath: str, algorithm: str = "sha256") -> str:
    """Calculate cryptographic hash of a file's contents"""
    hash_func = getattr(hashlib, algorithm)()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return ""

def format_bytes(size: int) -> str:
    """Convert byte size to human-readable format (KB, MB, GB, etc.)"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def calculate_speed(size_bytes: int, duration_sec: float) -> str:
    """Calculate transfer speed in appropriate units"""
    if duration_sec <= 0:
        return "∞ B/s"
    
    speed = size_bytes / duration_sec
    for unit in ['B/s', 'KB/s', 'MB/s', 'GB/s']:
        if speed < 1024.0:
            return f"{speed:.2f} {unit}"
        speed /= 1024.0
    return f"{speed:.2f} TB/s"

def safe_filename(filename: str) -> str:
    """Sanitize filename to remove potentially dangerous characters"""
    keepchars = (' ', '.', '_', '-')
    return "".join(c for c in filename if c.isalnum() or c in keepchars).rstrip()

def find_files(directory: str, extensions: List[str] = None) -> List[str]:
    """Find all files in directory with optional extension filter"""
    if not os.path.isdir(directory):
        print(f"❌ Directory not found: {directory}")
        return []
    
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if extensions:
                if any(filename.lower().endswith(ext) for ext in extensions):
                    files.append(os.path.join(root, filename))
            else:
                files.append(os.path.join(root, filename))
    return files

# ======================
# SECURITY UTILITIES
# ======================

def generate_key() -> str:
    """Generate a Fernet encryption key for message security"""
    return Fernet.generate_key().decode()

def encrypt_message(message: str, key: str) -> str:
    """Encrypt a message using Fernet symmetric encryption"""
    try:
        f = Fernet(key.encode())
        return f.encrypt(message.encode()).decode()
    except Exception as e:
        print(f"❌ Encryption failed: {e}")
        return message

def decrypt_message(encrypted: str, key: str) -> str:
    """Decrypt a Fernet-encrypted message"""
    try:
        f = Fernet(key.encode())
        return f.decrypt(encrypted.encode()).decode()
    except Exception as e:
        print(f"❌ Decryption failed: {e}")
        return encrypted

def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
    """Securely hash a password with optional salt"""
    if not salt:
        salt = os.urandom(16).hex()
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        100000
    ).hex(), salt

# ======================
# TIME UTILITIES
# ======================

def format_timestamp(timestamp: float) -> str:
    """Format Unix timestamp to human-readable date/time"""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def time_since(timestamp: float) -> str:
    """Get human-readable relative time (e.g., '5 minutes ago')"""
    seconds = time.time() - timestamp
    intervals = (
        ('year', 31536000),
        ('month', 2592000),
        ('week', 604800),
        ('day', 86400),
        ('hour', 3600),
        ('minute', 60),
        ('second', 1)
    )
    
    for name, divisor in intervals:
        value = seconds // divisor
        if value >= 1:
            return f"{int(value)} {name}{'s' if value != 1 else ''} ago"
    return "just now"

# ======================
# UI/UX UTILITIES
# ======================

def clear_screen():
    """Clear the terminal/console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display ASCII art application header"""
    print(r"""
__        __   _                                     
\ \      / /__| | ___ ___  _ __ ___   ___     
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \   
  \ V  V /  __/ | (_| (_) | | | | | |  __/  
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|   
                                                    

""")
    print("🔗 Secure P2P File Sharing & Chat\n")

def get_random_emoji() -> str:
    """Return a random emoji for visual interest"""
    emojis = ["✨", "⚡", "🎯", "🔑", "🔒", "🔓", "📡", "🌐", "🖥️", "💾", "📁", "📨", "📬"]
    return random.choice(emojis)

def animate_text(text: str, delay: float = 0.05):
    """Animate text printing with delay between characters"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_color_scheme():
    """Return the application color scheme"""
    return {
        'primary': '#6a1b9a',
        'secondary': '#0288d1',
        'background': '#f5f5f5',
        'text': '#212121',
        'accent': '#ffab00',
        'success': '#388e3c',
        'error': '#d32f2f',
        'chat_bg': '#ffffff',
        'chat_fg': '#000000'
    }

def apply_theme(widget, theme_type="default"):
    """Apply themed colors to widgets"""
    colors = get_color_scheme()
    if theme_type == "primary":
        widget.config(bg=colors['primary'], fg='white')
    elif theme_type == "secondary":
        widget.config(bg=colors['secondary'], fg='white')
    elif theme_type == "accent":
        widget.config(bg=colors['accent'], fg='white')
    elif theme_type == "success":
        widget.config(bg=colors['success'], fg='white')
    elif theme_type == "error":
        widget.config(bg=colors['error'], fg='white')
    elif theme_type == "chat":
        widget.config(bg=colors['chat_bg'], fg=colors['chat_fg'])
    else:
        widget.config(bg=colors['background'], fg=colors['text'])

# ======================
# VALIDATION UTILITIES
# ======================

def validate_config(config: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate configuration dictionary structure and values"""
    required = {
        'PORT': (int, lambda x: 1024 <= x <= 65535),
        'CHAT_PORT': (int, lambda x: 1024 <= x <= 65535),
        'BUFFER_SIZE': (int, lambda x: x >= 1024),
        'SHARED_FOLDER': (str, lambda x: os.path.exists(x))
    }
    
    for key, (type_check, validator) in required.items():
        if key not in config:
            return False, f"Missing config key: {key}"
        if not isinstance(config[key], type_check):
            return False, f"Invalid type for {key}, expected {type_check.__name__}"
        if not validator(config[key]):
            return False, f"Invalid value for {key}: {config[key]}"
    
    return True, "Config is valid"

def validate_file_path(path: str) -> bool:
    """Validate that a file path exists and is safe to access"""
    try:
        path = os.path.normpath(path)
        return os.path.exists(path) and os.path.isfile(path)
    except Exception:
        return False

def check_dependencies() -> bool:
    """Check if required Python packages are installed"""
    try:
        import tkinter
        import PIL
        import ttkthemes
        import cryptography
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {str(e)}")
        print("Please install required packages:")
        print("pip install pillow ttkthemes sv-ttk cryptography")
        return False

# ======================
# MISC UTILITIES
# ======================

def generate_id(length: int = 8) -> str:
    """Generate a random alphanumeric ID"""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(chars) for _ in range(length))

def retry_operation(operation: Callable, max_attempts: int = 3, 
                   delay: float = 1.0, **kwargs) -> Any:
    """Retry an operation with exponential backoff"""
    for attempt in range(1, max_attempts + 1):
        try:
            return operation(**kwargs)
        except Exception as e:
            if attempt == max_attempts:
                raise
            time.sleep(delay * (2 ** (attempt - 1)))
    return None

def measure_time(func: Callable) -> Callable:
    """Decorator to measure function execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ Function '{func.__name__}' took {end - start:.2f} seconds")
        return result
    return wrapper
