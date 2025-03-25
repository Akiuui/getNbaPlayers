from flask import Blueprint, jsonify, request, abort
import logging
import os

from services import fetchAndSavePlayers, getRosterById

players_bp = Blueprint("nba", __name__)

@players_bp.route("/populate", methods=["POST"])
def populate():
      
    authKey = request.headers.get("Authorization", "").strip()
    
    if not authKey or authKey != os.environ.get("AUTH").strip():
        abort(401, description="Unauthorized access")

    logging.info("Passed the authorization")

    inserted = fetchAndSavePlayers()

    return jsonify({"Success": f"Inserted {inserted} elements"}), 200

@players_bp.route("/getRoster", methods=["GET"])
def getRoster():

    teamId = request.args.get("teamId", "").strip()

    if teamId == "" or not teamId:
        abort(400, description="teamId is required")
        # print("asd")
        # roster = getRoster()
    else:
        roster = getRosterById(teamId)

    return jsonify(roster), 200
