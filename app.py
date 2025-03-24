from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient, errors

import os
import logging

from fetchers import fetchRoster
from formatter import formatPlayer
from static.staticIdsByCode import teamIdByCode

load_dotenv()
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

@app.route("/populate", methods=["POST"])
def savePlayers():
    authKey = request.headers.get("Authorization")
    
    if authKey==None or authKey != os.environ.get("AUTH"):
         return jsonify({"AuthError": "Unauthorized access"}), 401

    logging.info("Passed the auth")

    try:
        logging.info("Trying to connect to Mongo")
        client = MongoClient(os.environ.get("MONGO_KEY"), tls=True)
    except Exception as e:
        logging.info(f"There has been an exception! {e.args}")
        logging.info(f"The class! {e.__class__}")
        return jsonify({"error": "Could not connect to MongoDB"}), 500


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
               logging.error(f"id: {id}, has not been saved succesfully")

            inserted+=len(result.inserted_ids)
        except errors.BulkWriteError :
            logging.info("Duplicate id found skipping insertion")
        except Exception as e:
            logging.error(f"Exception: {e}")

    return jsonify({"Success": f"Inserted {inserted} elements"})


if __name__=="__main__":
    from waitress import serve
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 8006))
    serve(app, host="0.0.0.0", port=port)