def presence(rpc, client = None, data = None, content_data = None, config = None):
    rpc.update(
        state = "Launching...",
        large_image = "game_icon",
        large_text = "VALORANT",
    )