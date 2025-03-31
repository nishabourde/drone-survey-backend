from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI

fleet_bp = Blueprint("fleet", __name__)
client = MongoClient(MONGO_URI)
db = client["drone_survey"]

@fleet_bp.route("/drones", methods=["POST"])
def create_drone():
    data = request.json
    db.drones.insert_one(data)
    return jsonify({"message": "Drone added successfully"}), 201

@fleet_bp.route("/drones", methods=["GET"])
def get_drones():
    drones = list(db.drones.find({}))
    for drone in drones:
        drone["_id"] = str(drone["_id"])
    return jsonify(drones)

@fleet_bp.route("/drones/<drone_id>", methods=["PUT"])
def update_drone(drone_id):
    try:
        data = request.json

        if "_id" in data:
            data.pop("_id") 

        result = db.drones.update_one({"_id": ObjectId(drone_id)}, {"$set": data})

        if result.matched_count == 0:
            return jsonify({"message": "Drone not found"}), 404
        
        return jsonify({"message": "Drone updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fleet_bp.route("/drones/<drone_id>", methods=["DELETE"])
def delete_drone(drone_id):
    db.drones.delete_one({"_id": ObjectId(drone_id)})
    return jsonify({"message": "Drone deleted successfully"})
