from flask import  Blueprint, jsonify, request
from src.database.db_mysql import db, dataToJson
main = Blueprint('operative_system_blueprint',__name__)

@main.route('/', methods=['GET'])
def route_main():
    cursor = db.connection.cursor()
    sql = f'SELECT id, name, version, creation_date, last_modified_date, enabled FROM operative_system'
    cursor.execute(sql)
    result = cursor.fetchall()
    data = dataToJson(cursor.description, result)
    return jsonify(data), 200
