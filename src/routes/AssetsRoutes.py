from flask import  Blueprint, jsonify, request
from src.database.db_mysql import db, dataToJson
main = Blueprint('assets_blueprint',__name__)

@main.route('/', methods=['GET'])
def getAll():
    cursor = db.connection.cursor()
    sql = """SELECT
        a.id as "key",
        a.id,
        a.name,
        a.host,
        a.status,
        a.last_modified_date,
        a.operative_system_id,
        os.name as operative_system
    FROM
        asset a
        inner join operative_system os on os.id = a.operative_system_id
    WHERE
        a.enabled = true
    ORDER by
        a.last_modified_date DESC
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    data = dataToJson(cursor.description, result)
    return jsonify(data), 200

@main.route('/create', methods=['POST'])
def create():
    cursor = db.connection.cursor()
    body = request.get_json()    
    sql = f"""
    INSERT INTO
        asset (name, host, status, operative_system_id)
    VALUES
        (
            "{ body ['name'] }",
            "{ body ['host'] }",
            { body ['status'] },
            { body ['operative_system_id'] }
        )

    """
    sqlUser = f"""
        INSERT INTO asset_credentials (user, password, host)
        VALUES 
        (
            "{ body ['user'] }",
            "{ body ['password']}",
            "{ body ['host'] }"
        )
        """
    try:
        cursor.execute(sql)
        cursor.execute(sqlUser)
        db.connection.commit()
        return jsonify({'message': '¡Activo creado!'}), 201
    except Exception as e:
        db.connection.rollback()  # Revertir cambios en caso de error
        return jsonify({'message': "Ocurrio un error al guardar la información",'error': str(e)}), 500
    finally:
        cursor.close()

# @main.route('/createCredentials', methods=['POST'])
# def createCredentials():
#     cursor = db.connection.cursor()
#     body = request.get_json()    

#     sql = f"""
#     INSERT INTO
#         asset_credentials (user, host, password)
#     VALUES
#         (
#             "{ body ['user'] }",
#             "{ body ['host'] }",
#             "{ body ['password']}",
#         )
#     """

#     try:
#         cursor.execute(sql)
#         db.connection.commit()
#         return jsonify({'message': 'usuario guardado!'}), 201
#     except Exception as e:
#         db.connection.rollback()  # Revertir cambios en caso de error
#         return jsonify({'message': "Ocurrio un error al guardar la información",'error': str(e)}), 500
#     finally:
#         cursor.close()
