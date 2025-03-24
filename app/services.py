from flask import jsonify
from pymongo import MongoClient, errors
from static.staticIdsByCode import teamIdByCode
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