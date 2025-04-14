import os
import sys
import time
from gui import start_gui
from config import config
from animation import show_startup_animation
from utils import clear_screen, display_header, check_dependencies

def setup_environment():
    """Create necessary directories and validate permissions"""
    try:
        os.makedirs(config.SHARED_FOLDER, exist_ok=True)
        test_file = os.path.join(config.SHARED_FOLDER, '.permission_test')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True, f"✔️ Environment ready (Shared folder: {config.SHARED_FOLDER})"
    except PermissionError:
        return False, f"❌ Permission denied for shared folder: {config.SHARED_FOLDER}"
    except Exception as e:
        return False, f"❌ Environment setup failed: {str(e)}"

def main():
    """Main application entry point"""
    try:
        clear_screen()
        display_header()
        show_startup_animation()
        
        if not check_dependencies():
            time.sleep(3)
            sys.exit(1)
        
        success, message = setup_environment()
        print(f"\n{message}")
        if not success:
            time.sleep(3)
            sys.exit(1)
        
        print("\n🚀 Starting P2P Share application...")
        time.sleep(1)
        start_gui()
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Critical error: {str(e)}")
        import traceback
        traceback.print_exc()
        time.sleep(5)
        sys.exit(1)

if __name__ == "__main__":
    main()