from ...presence_utilities import Utilities
from .away import presence as away

def presence(rpc, client = None, data = None, content_data = None, config = None):
    is_afk = data["isIdle"]
    if is_afk:
        away(rpc, client, data, content_data, config)
    
    else:
        party_state, party_size = Utilities.build_party_state(data)
        data["MapID"] = data["matchMap"]
        map_name = Utilities.fetch_map_data(data, content_data)
        team = content_data["team_image_aliases"][data["customGameTeam"]] if data["customGameTeam"] in content_data["team_image_aliases"] else "game_icon_white"
        team_patched = content_data["team_aliases"][data["customGameTeam"]] if data["customGameTeam"] in content_data["team_aliases"].keys() else None
        
        if team_patched == "TeamOne":
            team_patched = "Defender"
        elif team_patched == "TeamTwo":
            team_patched = "Attacker"
        elif team_patched == "TeamSpectate":
            team_patched = "Observer"
        elif team_patched == "TeamOneCoaches":
            team_patched = "Defender Coach"
        elif team_patched == "TeamTwoCoaches":
            team_patched = "Attacker Coach"
        
        rpc.update(
            state = party_state,
            details = "Creating a Custom Game",
            large_image = f"splash_{map_name.lower()}",
            large_text = "Choosing " + map_name,
            small_image = team,
            small_text = team_patched,
            party_size = party_size,
            party_id = data["partyId"]
        )