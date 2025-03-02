from .ingame_presences.session import Game_Session
from .ingame_presences.range import Range_Session
from valclient.exceptions import PhaseError
from ...utilities.logging import Logger

def presence(rpc, client = None, data = None, content_data = None):
    try:
        coregame = client.coregame_fetch_player()
        
        if coregame is not None:
            match_id = coregame["MatchID"]
            if data["provisioningFlow"] != "ShootingRange":
                try:
                    session = Game_Session(rpc, client, match_id, content_data)
                    session.main_loop()
                except Exception as e:
                    Logger.debug("presence (ingame.py): " + str(e))
                    pass
            else:
                session = Range_Session(rpc, client, data, match_id, content_data)
                session.main_loop()
                
    except PhaseError:
        Logger.debug("presence (ingame): " + str(e))
        pass