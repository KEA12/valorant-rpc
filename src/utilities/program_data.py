import os, sys, ctypes, json

from .filepath import Filepath

class Program_data:
    
    installs_path = os.path.expandvars("%PROGRAMDATA%\\valorant-tools\\installs.json")
    
    @staticmethod
    def update_file_location():
        Program_data.check_for_folder()
        if getattr(sys, 'frozen', False):
            path = sys.executable
        else:
            ctypes.windll.user32.MessageBoxW(0, u"Running in a Testing Environment, cannot update installation path\n\nPress OK to continue.", u"Warning (VALORANT-RPC)", 48)
            path = None
            
        if path is not None:
            installs = Program_data.fetch_installs()
            installs["valorant-rpc"] = path
            Program_data.modify_installs(installs)
            
    @staticmethod
    def modify_installs(payload):
        with open(Program_data.installs_path, "w") as f:
            json.dump(payload, f)
            
        return Program_data.fetch_installs()
            
    @staticmethod
    def fetch_installs():
        try:
            with open(Program_data.installs_path) as f:
                installs = json.load(f)
                return installs
        except:
            return Program_data.create_installs_file()
        
    @staticmethod
    def create_installs_file():
        with open(Program_data.installs_path, "w") as f:
            payload = {}
            json.dump(payload, f)
            
        return Program_data.fetch_installs()
        
    @staticmethod
    def check_for_folder():
        programdata_folder = Filepath.get_programdata_folder()
        if not os.path.isdir(programdata_folder):
            os.makedirs(programdata_folder)