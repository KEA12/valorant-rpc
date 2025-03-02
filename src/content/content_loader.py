import requests

class Loader:
    
    @staticmethod
    def fetch(endpoint = "/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}?language=en-US")
        return data.json()
    
    @staticmethod
    def load_all_content(client):
        content_data = {
            "agents": [],
            "maps": [],
            "modes": [],
            "comp_tiers": [],
            "season": {},
            "queue_aliases": {
                "newmap": "New Map",
                "competitive": "Competitive",
                "unrated": "Unrated",
                "spikerush": "Spike Rush",
                "deathmatch": "Deathmatch",
                "ggteam": "Escalation",
                "onefa": "Replication",
                "custom": "Custom",
                "snowball": "Snowball Fight",
                "swiftplay": "Swiftplay",
                "hurm": "Team Deathmatch",
                "premier-tournament": "Premier",
                "": "Custom Game",
            },
            "custom_mode_aliases": {
                "/Game/GameModes/Bomb/BombGameMode.BombGameMode_C": "Standard",
                "/Game/GameModes/_Development/Swiftplay_EndOfRoundCredits/Swiftplay_EoRCredits_GameMode.Swiftplay_EoRCredits_GameMode_C": "Swiftplay",
                "/Game/GameModes/QuickBomb/QuickBombGameMode.QuickBombGameMode_C": "Spike Rush",
                "/Game/GameModes/HURM/HURMGameMode.HURMGameMode_C": "Team Deathmatch",
                "/Game/GameModes/GunGame/GunGameTeamsGameMode.GunGameTeamsGameMode_C": "Escalation",
                "/Game/GameModes/Deathmatch/DeathmatchGameMode.DeathmatchGameMode_C": "Deathmatch"
            },
            "team_aliases": {
                "TeamOne": "Defender",
                "TeamTwo": "Attacker",
                "TeamSpectate": "Observer",
                "TeamOneCoaches": "Defender Coach",
                "TeamTwoCoaches": "Attacker Coach",
            },
            "team_image_aliases": {
                "TeamOne": "team_defender",
                "TeamTwo": "team_attacker",
                "Red": "team_defender",
                "Blue": "team_attacker",
            },
            "modes_with_icons": ["ggteam","onefa","snowball","spikerush","unrated","deathmatch","swiftplay","hurm", "premier-tournament"]
        }
        all_content = client.fetch_content()
        agents = Loader.fetch("/agents")["data"]
        maps = Loader.fetch("/maps")["data"]
        modes = Loader.fetch("/gamemodes")["data"]
        comp_tiers = Loader.fetch("/competitivetiers")["data"][-1]["tiers"]
        
        
        for season in all_content["Seasons"]:
            if season["IsActive"] and season["Type"] == "act":
                content_data["season"] = {
                    "competitive_uuid": season["ID"],
                    "season_uuid": season["ID"],
                    "display_name": season["Name"]
                }
                
        for agent in agents:
            content_data["agents"].append({
                "uuid": agent["uuid"],
                "display_name": agent["displayName"],
                "internal_name": agent["developerName"]
            })
            
        for game_map in maps:
            content_data["maps"].append({
                "uuid": game_map["uuid"],
                "display_name": game_map["displayName"],
                "path": game_map["mapUrl"],
                "internal_name": game_map["mapUrl"].split("/")[-1]
            })
            
        for mode in modes:
            content_data["modes"].append({
                "uuid": mode["uuid"],
                "display_name": mode["displayName"],
            })
        content_data["modes"].append({
            "uuid": "premier-tournament",
            "display_name": "Premier",
        })
            
        for tier in comp_tiers:
            content_data["comp_tiers"].append({
                "display_name": tier["tierName"],
                "id": tier["tier"]
            })
            
            
        return content_data