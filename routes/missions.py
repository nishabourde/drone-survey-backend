
from bson import ObjectId
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from config import MONGO_URI
from flask_cors import CORS 

missions_bp = Blueprint("missions", __name__)
CORS(missions_bp)  

client = MongoClient(MONGO_URI)
db = client["drone_survey"]

@missions_bp.route("/missions", methods=["POST"])
def create_mission():
    data = request.json

    if not data.get("name") or not data.get("status"):
        return jsonify({"error": "Mission name and status are required"}), 400

    result = db.missions.insert_one(data)
    
    data["_id"] = str(result.inserted_id)  
    return jsonify({"message": "Mission created successfully", "mission": data}), 201

@missions_bp.route("/missions/<mission_id>", methods=["PUT"])
def update_mission(mission_id):
    try:
        data = request.json

        if "_id" in data:
            data.pop("_id") 

        result = db.missions.update_one({"_id": ObjectId(mission_id)}, {"$set": data})

        if result.matched_count == 0:
            return jsonify({"message": "Mission not found"}), 404
        
        return jsonify({"message": "Mission updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@missions_bp.route("/missions", methods=["GET"])
def get_missions():
    missions = list(db.missions.find({}))

    for mission in missions:
        mission["_id"] = str(mission["_id"]) 

    return jsonify(missions)


@missions_bp.route("/missions/<mission_id>", methods=["DELETE"])
def delete_mission(mission_id):
    result = db.missions.delete_one({"_id": ObjectId(mission_id)})
    if result.deleted_count == 1:
        return jsonify({"message": "Mission deleted successfully"}), 200
    else:
        return jsonify({"error": "Mission not found"}), 404