import os, json

from .logging import Logger

class Riot_Client_Services:
    
    @staticmethod
    def get_rcs_path():
        riot_installs_path = os.path.expandvars("%PROGRAMDATA%\\Riot Games\\RiotClientInstalls.json")
        try:
            with open(riot_installs_path, "r") as f:
                client_installs = json.load(f)
                rcs_path = os.path.abspath(client_installs["rc_default"])
                if not os.access(rcs_path, os.X_OK):
                    return None
                return rcs_path
        except FileNotFoundError as e:
            Logger.debug("get_rcs_path: " + str(e))
            return None