import os, logging

from .filepath import Filepath

class Logger:
    
    @staticmethod
    def create_logger():
        os.makedirs(Filepath.get_path(os.path.join(Filepath.get_appdata_folder())), exist_ok = True)
        logging.basicConfig(filename = Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'rpc.log')),
                            filemode = "w+",
                            format = '%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level = logging.DEBUG)
        
        logger = logging.getLogger('rpc')
        logger.debug("Created Log")
        
    @staticmethod
    def debug(data):
        logger = logging.getLogger('rpc')
        logger.debug(data)