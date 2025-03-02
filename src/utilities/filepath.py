import sys, os
from pathlib import Path

class Filepath:
    
    @staticmethod
    def get_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    @staticmethod
    def get_appdata_folder():
        return Filepath.get_path(os.path.join(os.getenv('APPDATA'), 'valorant-rpc'))
    
    @staticmethod
    def get_log_file_path():
        user_profile = Path(os.getenv("USERPROFILE", ""))
        log_file_path = user_profile / "AppData" / "Local" / "VALORANT" / "Saved" / "Logs" / "ShooterGame.log"

        return str(log_file_path)