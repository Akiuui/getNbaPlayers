def formatPlayer(player, teamId):
    
    player["_id"] = player["id"]
    player["teamId"] = teamId
    del player["id"]

    return player