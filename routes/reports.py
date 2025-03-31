from flask import Blueprint, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from config import MONGO_URI

reports_bp = Blueprint("reports", __name__)
client = MongoClient(MONGO_URI)
CORS(reports_bp) 

db = client["drone_survey"]

@reports_bp.route('/reports', methods=['GET'])
def get_reports():
    reports = list(db.reports.find({}, {'_id': 0})) 
    return jsonify(reports)
