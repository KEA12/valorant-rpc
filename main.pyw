import ctypes, traceback, os
from src.startup import Startup

if __name__ == '__main__':
    try:
        app = Startup()
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, f"An error occured during execution.\n\n({e})\n\nPress OK to exit.", u"Error (VALORANT-RPC)", 16)
        traceback.print_exc()
        os._exit(1)