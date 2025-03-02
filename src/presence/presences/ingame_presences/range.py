import time
from ..menu_presences.away import presence as away
from ...presence_utilities import Utilities
from ....utilities.filepath import Filepath
from ....utilities.logging import Logger

class Range_Session:
    def __init__(self, rpc, client, data, match_id, content_data):
        self.rpc = rpc
        self.client = client
        self.content_data = content_data
        self.match_id = match_id
        self.puuid = self.client.puuid
        
        data["MapID"] = "/Game/Maps/Poveglia/Range"
        self.start_time = time.time()
        self.map_name = Utilities.fetch_map_data(data, content_data)
        self.map_image = "splash_range"
        self.small_image = ""
        self.small_text = ""
        self.log_file_path = Filepath.get_log_file_path()
    
        
        
    def main_loop(self):
        presence = self.client.fetch_presence()
        while presence is not None and presence["sessionLoopState"] == "INGAME":
            try:
                presence = self.client.fetch_presence()
                self.agent = Utilities.custom_get_agent(self.log_file_path)
                self.agent_uuid = Utilities.fetch_agent_internal_name(self.agent, self.content_data)
                self.small_image, self.small_text = Utilities.fetch_agent_data(self.agent_uuid, self.content_data)
                is_afk = presence["isIdle"]
                if is_afk:
                    away(self.rpc, self.client, presence, self.content_data, self.config)
                else:
                    party_state, party_size = Utilities.build_party_state(presence)
                    
                    self.rpc.update(
                        state = party_state,
                        details = "Practicing on " + self.map_name,
                        start = self.start_time,
                        large_image = self.map_image,
                        large_text = "Practicing on " + self.map_name,
                        small_image = self.small_image,
                        small_text = "Playing as " + self.small_text,
                        party_size = party_size,
                        party_id = presence["partyId"]
                    )
                
                time.sleep(5)
            except Exception as e:
                Logger.debug("main_loop (range.py): " + str(e))
                return