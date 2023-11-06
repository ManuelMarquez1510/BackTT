from flask import  Blueprint, jsonify, request
from src.database.db_mysql import db, dataToJson
main = Blueprint('security_policies_blueprint',__name__)

@main.route('/', methods=['GET'])
def getAll():
    cursor = db.connection.cursor()
    sql = """SELECT
        p.id as "key",
        p.id,
        p.name,
        p.version,
        p.last_modified_date,
        p.operative_system_id,
        os.name as operative_system
    FROM
        policy p
        inner join operative_system os on os.id = p.operative_system_id
    WHERE
        p.enabled = true
    ORDER by
        p.last_modified_date DESC
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    data = dataToJson(cursor.description, result)
    return jsonify(data), 200

@main.route('/getByIdSO/<int:id>', methods=['GET'])
def getPoliciesById(id):
    cursor = db.connection.cursor()
    sql = f"""SELECT
        p.id as "key",
        p.id,
        p.name,
        p.version,
        p.last_modified_date,
        p.operative_system_id,
        os.name as operative_system
    FROM
        policy p
        inner join operative_system os on os.id = p.operative_system_id
    WHERE
        p.enabled = true
    AND
        p.operative_system_id = {id}
    ORDER by
        p.name ASC
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    data = dataToJson(cursor.description, result)
    return jsonify(data), 200

@main.route('/create', methods=['POST'])
def create():
    cursor = db.connection.cursor()
    body = request.get_json()
    reference_value = f'"{body["reference"]}"' if "reference" in body and body["reference"] else "NULL"
    

    # Verifica si se proporcionaron todos los datos necesarios
    # if "rules" not in body or body['rules'] is None :
    #     return jsonify({'message': 'Se requieren reglas para asignar a la política'}), 400


    sql = f"""
    INSERT INTO
        policy (name, version, reference, operative_system_id)
    VALUES
        (
            "{ body ['name'] }",
            "{ body ['version'] }",
            { reference_value },
            { body ['operative_system_id'] }
        )
    """

    try:
        cursor.execute(sql)
        db.connection.commit()
        return jsonify({'message': 'Política creada!'}), 201
    except Exception as e:
        db.connection.rollback()  # Revertir cambios en caso de error
        return jsonify({'message': "Ocurrio un error al guardar la información",'error': str(e)}), 500
    finally:
        cursor.close()
