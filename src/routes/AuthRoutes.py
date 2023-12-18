from flask import  Blueprint, jsonify, request
from src.database.db_mysql import db, dataToJson

main = Blueprint('auth_blueprint',__name__)

@main.route('/login',  methods=['POST'])
def route_main():
    try:
        with db.connection.cursor() as cursor:
            body = request.get_json()
            getUser = """
            SELECT
                *
            FROM
                user u
            WHERE
                u.enabled = true
                AND u.name = %s
                AND u.password = %s
            LIMIT 1
            """
            
            cursor.execute(getUser,(body['username'], body['password']))
            result = cursor.fetchall()
            data = dataToJson(cursor.description, result)

        if(not len(data)):
            return jsonify({'message':"Usuario o contraseña incorrectos, intente de nuevo"}), 404

        return jsonify({'message':"Credenciales correctas"}), 200

    except Exception as e:
        db.connection.rollback()
        return jsonify({'message': "Ocurrió un error inesperado", 'error': str(e)}), 500
