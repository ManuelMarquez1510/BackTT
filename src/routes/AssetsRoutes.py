from flask import  Blueprint, jsonify, request
from src.database.db_mysql import db, dataToJson
from src.models.internal_api import init_connection
main = Blueprint('assets_blueprint',__name__)

@main.route('/', methods=['GET'])
def getAll():
    cursor = db.connection.cursor()
    sql = """
   SELECT
    a.id as "key",
    a.id,
    a.name,
    a.host,
    a.status,
    a.last_modified_date,
    a.operative_system_id,
    os.name as operative_system,
    g.name as group_name
FROM
    asset a
    INNER JOIN operative_system os ON os.id = a.operative_system_id
    LEFT JOIN `group` g ON a.group_id = g.id
WHERE
    a.enabled = true
ORDER BY
    a.last_modified_date DESC;

    """
    cursor.execute(sql)
    result = cursor.fetchall()
    data = dataToJson(cursor.description, result)
    return jsonify(data), 200

@main.route('/create', methods=['POST'])
def create():
    cursor = db.connection.cursor()
    body = request.get_json() 
    port_value = f'{body["port"]}' if "port" in body and body["port"] else "undefined"
    # print(body)   
    sql = f"""
    INSERT INTO
        asset (name, host, status, operative_system_id, group_id)
    VALUES
        (
            "{ body ['name'] }",
            "{ body ['host'] }",
            { body ['status'] },
            { body ['operative_system_id'] },
            { body ['group_id'] }
        )

    """
    if (port_value == "undefined"):
        resp=init_connection(body['host'], body['user'],body['password'])
    else: 
        resp=init_connection(body['host'], body['user'],body['password'], port_value)
    print("resp: ", resp.get("Error"))
    # sqlUser = f"""
    #     INSERT INTO asset_credentials (user, password, host)
    #     VALUES 
    #     (
    #         "{ body ['user'] }",
    #         "{ body ['password']}",
    #         "{ body ['host'] }"
    #     )
    #     """
    try:
        if (resp.get("Error")==0):
            cursor.execute(sql)
            db.connection.commit()
            return jsonify({'message': 'Activo creado!', 'Error': '0'}), 201
        else:
            db.connection.rollback()  # Revertir cambios en caso de error
            return jsonify({'message': '¡Host invalido!', 'Error': '1'}), 201
        
    except Exception as e:
        db.connection.rollback()  # Revertir cambios en caso de error
        return jsonify({'message': "Ocurrio un error al guardar la información",'error': str(e)}), 500
    finally:
        cursor.close()