import os, json

from valclient.client import Client
from ..filepath import Filepath
from ...mapping.reader import Reader
from ..logging import Logger


default_config = {
    "region": ["", Client.fetch_regions()],
    "client_id": 1225506034576261131,
    "version": "v1.0.1"
}

class Config:
    
    @staticmethod
    def update_version(version):
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json")), "w") as f:
            data = default_config
            data["version"] = version
            json.dump(data, f)
        
    
    @staticmethod
    def fetch_config():
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json"))) as f:
                config = json.load(f)
                return config
        except Exception as e:
            Logger.debug("fetch_config: " + str(e))
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
    

    @staticmethod
    def check_config_version():
        if Reader.get_config_value("version") != default_config["version"]:
            Config.update_version(default_config["version"])
            return default_config["version"]
        return None