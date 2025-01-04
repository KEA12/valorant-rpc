import os, time, asyncio, ctypes, traceback

from pypresence import Presence as PyPresence
from pypresence.exceptions import InvalidPipe
from .presences import (ingame, menu, startup, pregame)
from ..content.content_loader import Loader
from ..utilities.logging import Logger

class Presence:
    def __init__(self, config):
        self.config = config
        self.client = None
        self.loaded = False
        try:
            self.rpc = PyPresence(client_id = "1225506034576261131")
            self.rpc.connect()
        except InvalidPipe as e:
            raise Exception("__init__ (presence.py): "  + str(e))
        self.content_data = {}
        
    
    def main_loop(self):
        while True:
            presence_data = self.client.fetch_presence()
            if presence_data is not None:
                self.update_presence(presence_data["sessionLoopState"], presence_data)
            else:
                os._exit(1)
                
            if not self.loaded:
                self.loaded = True
                self.content_data = Loader.load_all_content(self.client)
                
            time.sleep(5)
            
            
    def init_loop(self):
        try:
            self.content_data = Loader.load_all_content(self.client)
            presence_data = self.client.fetch_presence()
            
            if presence_data is not None:
                self.update_presence(presence_data["sessionLoopState"], presence_data)
                
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            self.main_loop()
    
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"An error has occured during execution:\n\n{e}\n\nPress OK to exit.", u"Error (VALORANT-RPC)", 16)
            traceback.print_exc()
            os._exit(1)
    
    def update_presence(self, ptype, data = None):
        presence_types = {
            "startup": startup,
            "MENUS": menu,
            "PREGAME": pregame,
            "INGAME": ingame
        }
        
        if ptype in presence_types.keys():
            presence_types[ptype].presence(self.rpc, client = self.client, data = data, content_data = self.content_data, config = self.config)