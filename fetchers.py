import requests
import datetime
import os

def fetchRoster(teamId):
    print(datetime.datetime.now().year)
    url = f"https://v2.nba.api-sports.io/players?team={teamId}&season={datetime.datetime.now().year-1}"
    headers = {
        'x-rapidapi-host': "v2.nba.api-sports.io",
        'x-rapidapi-key': os.environ.get("API-KEY")
    }
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        return res.json()
    else:
        return None