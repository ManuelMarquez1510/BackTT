from flask import  Blueprint, jsonify
from src.database.db_mysql import dataToJson
from src.services.AssetsService import get_assets_by_group, get_assets_by_id
main = Blueprint('diagnosis_blueprint',__name__)

@main.route('/diagnostic_asset/<int:id>', methods=['POST'])
def diagnostic_asset(id):
    data = get_assets_by_id(id)
    return jsonify({'message':'OK', 'data': data}), 200

@main.route('/diagnostic_group/<int:id>', methods=['POST'])
def diagnostic_group(id):
    data = get_assets_by_group(id)
    return jsonify({'message':'OK', 'data':data}), 200
