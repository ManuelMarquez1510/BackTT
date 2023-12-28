from flask import  Blueprint, jsonify
from src.database.db_mysql import dataToJson, db
from src.services.AssetsService import get_assets_by_group, get_assets_by_id
from src.models.internal_api import evaluate_assets

main = Blueprint('diagnosis_blueprint',__name__)

@main.route('/', methods=['GET'])
def getAll():
    cursor = db.connection.cursor()
    sql = """
    select
        d.id as "key",
        d.*,
        a.id as asset_id,
        a.name,
        a.host,
        p.id as policy_id,
        p.name as policy_name
    from
        diagnosis d
    inner join asset a on
        a.id = d.asset_id
    inner join `group` g on
        g.id = a.group_id
    inner join policy p ON
        p.id = g.policy_id
    where
        d.enabled = true
        and a.enabled = true
    ORDER BY
        last_modified_date DESC;
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    data = dataToJson(cursor.description, result)
    return jsonify(data), 200

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
