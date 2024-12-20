import os, json

from valclient.client import Client
from ..filepath import Filepath

default_config = {
    "region": ["", Client.fetch_regions()],
    "client_id": 1225506034576261131,
    "version": "1.0.0"
}

class Config:
    
    @staticmethod
    def fetch_config():
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json"))) as f:
                config = json.load(f)
                return config
        except:
            return Config.create_default_config()
            
    @staticmethod
    def create_default_config():
        if not os.path.exists(Filepath.get_appdata_folder()):
            os.mkdir(Filepath.get_appdata_folder())
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json")), "w") as f:
            json.dump(default_config, f)
        return Config.fetch_config()
    
    @staticmethod
    def modify_config(new_config):
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json")), "w") as f:
            json.dump(new_config, f)
            
        return Config.fetch_config()