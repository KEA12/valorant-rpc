import time

from valclient.exceptions import PhaseError
from ...presence_utilities import Utilities
from ....utilities.filepath import Filepath
from ..menu_presences.away import presence as away

class Game_Session:
    def __init__(self, rpc, client, match_id, content_data, config):
        self.rpc = rpc
        self.client = client
        self.config = config
        self.content_data = content_data
        self.match_id = match_id
        self.puuid = self.client.puuid
        self.start_time = time.time()
        self.large_text = ""
        self.large_image = ""
        self.small_text = ""
        self.small_image = ""
        self.mode_name = ""
        self.large_pref = ["map",["rank","agent","map"]]
        self.small_pref = ["agent",["rank","agent","map"]]
        self.custom = False
        self.log_file_path = Filepath.get_log_file_path()
        self.custom_game_mode = ""
        self.build_static_states()
        
    def build_static_states(self):
        presence = self.client.fetch_presence()
        try:
            coregame_data = self.client.coregame_fetch_match(self.match_id)
            if coregame_data["ProvisioningFlow"] == "CustomGame":
                self.custom = True
                self.custom_game_mode = Utilities.fetch_custom_mode_data(coregame_data, self.content_data, False)
        except PhaseError:
            raise Exception
        coregame_player_data = {}
        for player in coregame_data["Players"]:
            if player["Subject"] == self.puuid:
                coregame_player_data = player
                
        self.large_image, self.large_text = Utilities.get_content_preferences(self.client, self.large_pref, coregame_player_data, coregame_data, self.content_data)
        self.small_image, self.small_text = Utilities.get_content_preferences(self.client, self.small_pref, coregame_player_data, coregame_data, self.content_data)
        _, self.mode_name = Utilities.fetch_mode_data(presence, self.content_data)
        

    def main_loop(self):
        presence = self.client.fetch_presence()
        while presence is not None and presence["sessionLoopState"] == "INGAME":
            presence = self.client.fetch_presence()
            if self.custom:
                self.agent = Utilities.custom_get_agent(self.log_file_path)
                self.agent_uuid = Utilities.fetch_agent_internal_name(self.agent, self.content_data)
                self.small_image, self.small_text = Utilities.fetch_agent_data(self.agent_uuid, self.content_data)
            is_afk = presence["isIdle"]
            if is_afk:
                away(self.rpc, self.client, presence, self.content_data)
            else:
                party_state, party_size = Utilities.build_party_state(presence)
                my_score, other_score = presence["partyOwnerMatchScoreAllyTeam"], presence["partyOwnerMatchScoreEnemyTeam"]
                
                self.rpc.update(
                    state = party_state,
                    details = f"{self.mode_name} {self.custom_game_mode} // {my_score} - {other_score}",
                    start = self.start_time,
                    large_image = self.large_image,
                    large_text = "Playing on " + self.large_text,
                    small_image = self.small_image,
                    small_text = "Playing as " + self.small_text,
                    party_size = party_size,
                    party_id = presence["partyId"],
                    instance = True
                )
                
            time.sleep(5)