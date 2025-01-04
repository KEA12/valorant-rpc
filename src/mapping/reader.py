from .mappings import Mappings
from ..utilities.logging import Logger

class Reader:
    
    config = None
    
    @staticmethod
    def get_config_value(*keys):
        mapped_keys = [Reader.get_config_key(key) for key in keys]
        result = Reader.config
        for key in mapped_keys:
            result = result[key]
        return result
        
    @staticmethod
    def get_config_key(key):
        try:
            for k, value in Mappings["config"].items():
                if k == key:
                    return value
            return key
        except Exception as e:
            Logger.debug("get_config_key: " + str(e))
            return key