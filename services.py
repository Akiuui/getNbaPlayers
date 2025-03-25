from flask import jsonify, abort
from pymongo import MongoClient, errors
from staticIdsByCode import teamIdByCode
from fetchers import fetchRoster
from formatter import formatPlayer
import logging
import os

def ConnectToMongo():
    try:
        client = MongoClient(os.environ.get("MONGO_KEY"), tls=True)
    except Exception as e:
        logging.info(f"There has been an exception! {e.args}")
        return jsonify({"error": "Could not connect to MongoDB"}), 500

    return client

def getRoster():
    logging.info("Trying to connect to Mongo")
    client = ConnectToMongo()
    logging.info("Succesfully connected to mongoDb")

    db = client["NbaGames"]
    collection = db["NbaPlayers"]

    try:
        roster = collection.find({}) 
    except Exception as e:
        logging.error({"Exception":f"Mongo caused an exception: {e}"}) 

    roster = list(roster)

    if roster == None or roster == []:
        logging.error("Roster not found")
        abort(400, description="TeamId is not entered correctly")
    else:
        logging.info("Roster found")
    
    return roster

def getRosterById(teamId):

    logging.info("Trying to connect to Mongo")
    client = ConnectToMongo()
    logging.info("Succesfully connected to mongoDb")

    db = client["NbaGames"]
    collection = db["NbaPlayers"]

    try:
        roster = collection.find({"teamId": int(teamId)}) 
    except Exception as e:
        logging.error({"Exception":f"Mongo caused an exception: {e}"}) 

    roster = list(roster)

    if roster == None or roster == []:
        logging.error("Roster not found")
        abort(400, description="TeamId is not entered correctly")
    else:
        logging.info("Roster found")
    
    return roster


def fetchAndSavePlayers():
    logging.info("Trying to connect to Mongo")
    client = ConnectToMongo()
    logging.info("Succesfully connected to mongoDb")

    db = client["NbaGames"]
    collection = db["NbaPlayers"]

    collection.delete_many({})
    logging.info("Cleaned the collection")

    inserted = 0
    for id in teamIdByCode.values():
        try:
            roster = fetchRoster(id)

            formattedRoster = []
            for player in roster["response"]:
                formattedPlayer = formatPlayer(player, teamId=id)
                formattedRoster.append(formattedPlayer)

            result = collection.insert_many(formattedRoster, ordered=False)

            if not result.acknowledged:
               logging.error(f"TeamId: {id}, has not been saved succesfully")

            inserted+=len(result.inserted_ids)

        except errors.BulkWriteError :
            logging.info("Duplicate id found skipping insertion")
        except Exception as e:
            logging.error(f"Exception: {e}")

    return inserted