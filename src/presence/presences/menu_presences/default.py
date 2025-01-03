from .away import presence as away
from ...presence_utilities import Utilities

def presence(rpc, client = None, data = None, content_data = None, config = None):
    is_afk = data["isIdle"]
    if is_afk:
        away(rpc, client, data, content_data, config)
    
    else:
        party_state, party_size = Utilities.build_party_state(data)
        small_image, mode_name = Utilities.fetch_mode_data(data, content_data)
        small_text = mode_name
        
        if data["queueId"] == "competitive":
            small_image, small_text = Utilities.fetch_rank_data(client, content_data)
        
        rpc.update(
            state = party_state,
            details = f"Mode Select - {mode_name}",
            large_image = "game_icon",
            large_text = f"Level {data['accountLevel']}",
            small_image = small_image,
            small_text = small_text,
            party_size = party_size,
            party_id = data["partyId"]
        )