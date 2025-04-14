import os
import sys
from typing import Dict, Any
from pathlib import Path

DEFAULT_CONFIG: Dict[str, Any] = {
    'PORT': 5001,
    'CHAT_PORT': 5002,
    'BUFFER_SIZE': 16384,  # 16KB chunks
    'SOCKET_TIMEOUT': 30,
    'MAX_RETRIES': 3,
    'RETRY_DELAY': 2,
    'LOG_LEVEL': 'INFO',
}

class AppConfig:
    def __init__(self):
        self._validate_ports()
        self._setup_paths()
        
    def _validate_ports(self):
        # Validate the ports to be within the acceptable range
        for port in [DEFAULT_CONFIG['PORT'], DEFAULT_CONFIG['CHAT_PORT']]:
            if not 1024 <= port <= 65535:
                print(f"❌ Invalid port number: {port}. Must be between 1024-65535")
                sys.exit(1)
                
    def _setup_paths(self):
        # Set up the base and log directories, creating them if necessary
        self.BASE_DIR = Path(os.getcwd())
        self.SHARED_FOLDER = self.BASE_DIR / "shared_files"
        self._ensure_directory(self.SHARED_FOLDER)
        self.LOG_DIR = self.BASE_DIR / "logs"
        self._ensure_directory(self.LOG_DIR)
        
    def _ensure_directory(self, path: Path):
        # Ensure the directory exists and has the necessary permissions
        try:
            path.mkdir(exist_ok=True, parents=True)
            # Test if we can write to the directory
            test_file = path / '.permission_test'
            test_file.touch()
            test_file.unlink()
        except PermissionError:
            print(f"❌ Permission denied for directory: {path}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Failed to setup directory {path}: {str(e)}")
            sys.exit(1)

    def __getattr__(self, name):
        # Return the configuration setting or raise an error if not found
        if name in DEFAULT_CONFIG:
            return DEFAULT_CONFIG[name]
        raise AttributeError(f"Configuration '{name}' not found")

# Create the global config instance
config = AppConfig()

# Legacy access for configuration settings
PORT = config.PORT
CHAT_PORT = config.CHAT_PORT
BUFFER_SIZE = config.BUFFER_SIZE
SHARED_FOLDER = str(config.SHARED_FOLDER)

# ======================
# THEME CONFIGURATION
# ======================

THEME_CONFIG = {
    "current_theme": "light",
    "themes": {
        "light": {
            "primary": "#6a1b9a",
            "background": "#f5f5f5"
        },
        "dark": {
            "primary": "#9b59b6",
            "background": "#2c3e50"
        }
    }
}
