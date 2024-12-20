from ...presence_utilities import Utilities

def presence(rpc, client = None, data = None, content_data = None, config = None):
    party_state, party_size = Utilities.build_party_state(data)
    start_time = Utilities.iso8601_to_epoch(data['queueEntryTime'])
    small_image, mode_name = Utilities.fetch_mode_data(data, content_data)
    small_text = mode_name
    
    rpc.update(
        state = party_state, 
        details = f"Queue - {mode_name}",
        start = start_time,
        large_image = "game_icon_white",
        large_text = f"Level - {data['accountLevel']}",
        small_image = small_image,
        small_text = small_text,
        party_size = party_size,
        party_id = data["partyId"]
    )