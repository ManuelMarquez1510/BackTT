from flask import  Blueprint, jsonify
from src.database.db_mysql import db, dataToJson
main = Blueprint('rules_blueprint',__name__)

@main.route('/getByPolicyId/<int:id>', methods=['GET'])
def route_main(id):
    cursor = db.connection.cursor()
    sql = f"""SELECT
        r.id as "key",
        r.*
    FROM
        policy_rule pr
        inner join rule r on r.id = pr.rule_id
    WHERE
        r.enabled = true
        AND pr.policy_id = {id}
    ORDER BY
        r.title ASC"""
    cursor.execute(sql)
    result = cursor.fetchall()
    data = dataToJson(cursor.description, result)
    return jsonify(data), 200
