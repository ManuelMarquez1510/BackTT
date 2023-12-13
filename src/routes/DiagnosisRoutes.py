from flask import  Blueprint, jsonify
from src.database.db_mysql import dataToJson
from src.services.AssetsService import get_assets_by_group, get_assets_by_id
from src.models.internal_api import evaluate_assets

main = Blueprint('diagnosis_blueprint',__name__)

@main.route('/diagnostic_asset/<int:id>', methods=['POST'])
def diagnostic_asset(id):
    data = get_assets_by_id(id)
    evaluate_assets(data)
    return jsonify({'message':'OK', 'data': data}), 200

@main.route('/diagnostic_group/<int:id>', methods=['POST'])
def diagnostic_group(id):
    data = get_assets_by_group(id)
    evaluate_assets(data)
    return jsonify({'message':'OK', 'data':data}), 200
