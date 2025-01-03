import time

from ..presence_utilities import Utilities
from valclient.exceptions import PhaseError

def presence(rpc, client = None, data = None, content_data = None, config = None):
    party_state, party_size = Utilities.build_party_state(data)
    custom = False
    custom_game_mode = ""
    
    try:
        pregame = client.pregame_fetch_player()
        match_id = pregame["MatchID"]
        pregame_data = client.pregame_fetch_match(match_id)
        if pregame_data["ProvisioningFlowID"] == "CustomGame":
                custom = True
        puuid = client.puuid
        
        pregame_player_data = {}
        for player in pregame_data["AllyTeam"]["Players"]:
            if player["Subject"] == puuid:
                pregame_player_data = player
                
        pregame_end_time = (pregame_data['PhaseTimeRemainingNS'] // 1000000000) + time.time()
        
        
        agent_image, agent_name = Utilities.fetch_agent_data(pregame_player_data["CharacterID"], content_data)
        select_state = "Locked" if pregame_player_data["CharacterSelectionState"] == "locked" else "Hovering"
        _, mode_name = Utilities.fetch_mode_data(data, content_data)
        
        if custom:
            custom_game_mode = Utilities.fetch_custom_mode_data(pregame_data, content_data, True)
        
        rpc.update(
            state = party_state,
            details = f"Agent Select - {mode_name} {custom_game_mode}",
            end = pregame_end_time,
            large_image = agent_image,
            large_text = f"{select_state} - {agent_name}",
            party_size = party_size,
            party_id = data["partyId"]
        )
    
    except PhaseError:
        pass