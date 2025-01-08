import iso8601, re

from ..utilities.logging import Logger

class Utilities:
    
    @staticmethod
    def get_content_preferences(client, pref, player_data, coregame_data, content_data):
        for key in pref:
            if key == "map":
                gmap = Utilities.fetch_map_data(coregame_data, content_data)
                return f"splash_{gmap.lower()}", str(gmap)
            if key == "rank":
                return Utilities.fetch_rank_data(client, content_data)
            if key == "agent":
                return Utilities.fetch_agent_data(player_data["CharacterID"], content_data)

    
    @staticmethod
    def fetch_rank_data(client, content_data):
        try:
            mmr = client.fetch_mmr()["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][content_data["season"]["season_uuid"]]
        except Exception as e:
            Logger.debug("fetch_rank_data: " + str(e))
            return "rank_0", "Rank not found"
        rank_data = {}
        for tier in content_data["comp_tiers"]:
            if tier["id"] == mmr["CompetitiveTier"]:
                rank_data = tier
        rank_image = f"rank_{rank_data['id']}"
        rank_text = f"{rank_data['display_name']} - {mmr['RankedRating']}RR" + (f" // #{mmr['LeaderboardRank']}" if mmr['LeaderboardRank'] != 0 else "")
        
        return rank_image, rank_text
    

    @staticmethod
    def fetch_map_data(coregame_data, content_data):
        for gmap in content_data["maps"]:
            if gmap["path"] == coregame_data["MapID"]:
                return gmap["display_name"]
        return ""
    

    @staticmethod
    def fetch_agent_data(uuid, content_data):
        for agent in content_data["agents"]:
            if agent["uuid"] == uuid:
                agent_image = f"agent_{agent['display_name'].lower().replace('/','')}"
                agent_name = agent['display_name']
                return agent_image, agent_name
        return "rank_0", "?"
    
    @staticmethod
    def fetch_agent_internal_name(internal_name, content_data):
        for agent in content_data["agents"]:
            if agent["internal_name"] == internal_name:
                return agent["uuid"]
        return None
    
    
    @staticmethod
    def fetch_mode_data(data, content_data):
        image = f"mode_{data['queueId'] if data['queueId'] in content_data['modes_with_icons'] else 'discovery'}"
        mode_name = content_data['queue_aliases'][data['queueId']] if data["queueId"] in content_data["queue_aliases"] else "Custom Game"
        return image, mode_name

    @staticmethod
    def fetch_custom_mode_data(data, content_data, pregame = False):
        if pregame:
            mode_name = content_data['custom_mode_aliases'][data['Mode']] if data["Mode"] in content_data["custom_mode_aliases"] else "Standard"
        else:
            mode_name = content_data['custom_mode_aliases'][data['ModeID']] if data["ModeID"] in content_data["custom_mode_aliases"] else "Standard"
        return "(" + mode_name + ")"

    @staticmethod
    def custom_get_agent(log_file_path):
        log_entry_pattern = re.compile(
            r"LogPlayerController: Warning: \[.*?\] ClientRestart_Implementation\(.*?\) - "
            r"AcknowledgePawn\('(?P<agent>.*?)'\)"
        )
        agent = None

        with open(log_file_path, "r") as log_file:
            for line in log_file:
                match = log_entry_pattern.search(line)
                if match:
                    new_agent = match.group("agent")
                    agent = new_agent.split("_")[0]

        return agent    
    
    @staticmethod
    def build_party_state(data):
        party_state = "Solo"
        if data["partySize"] > 1:
            party_state = "In a Party"
        elif data["partyAccessibility"] == "OPEN":
            party_state = "Open Party"
            
        party_size = [data["partySize"], data["maxPartySize"]] if data["partySize"] > 1 or data["partyAccessibility"] == "OPEN" else None
        if party_size is not None:
            if party_size[0] == 0:
                party_size[0] = 1
            if party_size[1] < 1:
                party_size[1] = 1
        return party_state, party_size
    
    
    @staticmethod
    def iso8601_to_epoch(time):
        if time == "0001.01.01-00.00.00":
            return None
        split = time.split("-")
        split[0] = split[0].replace(".", "-")
        split[1] = split[1].replace(".", ":")
        split = "T".join(i for i in split)
        split = iso8601.parse_date(split).timestamp()
        return split