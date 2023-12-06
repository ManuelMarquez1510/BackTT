from flask import  Blueprint, jsonify, request
from src.database.db_mysql import db, dataToJson
main = Blueprint('groups_blueprint',__name__)

@main.route('/', methods=['GET'])
def getAll():
    cursor = db.connection.cursor()
    sql = """
    SELECT
        g.id as "key",
        g.id,
        g.name,
        g.creation_date,
        g.policy_id,
        p.name as policy,
        COUNT(a.id) as assets_quantity
    FROM
        `group` g
        INNER JOIN policy p ON p.id = g.policy_id
        LEFT JOIN asset a ON a.group_id = g.id
    WHERE
        g.enabled = true
    GROUP BY
        g.id
    ORDER BY
        g.last_modified_date asc
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    data = dataToJson(cursor.description, result)
    return jsonify(data), 200

@main.route('/create', methods=['POST'])
def create():
    try:
        with db.connection.cursor() as cursor:
            body = request.get_json()

            insert_group = "INSERT INTO `group` (name, policy_id) VALUES (%s, %s);"
            cursor.execute("START TRANSACTION")
            cursor.execute(insert_group, (body['name'], body['policy_id']))
            db.connection.commit()

        return jsonify({'message': 'Grupo creado!'}), 201
    
    except Exception as e:
        db.connection.rollback()
        return jsonify({'message': "Ocurrió un error inesperado", 'error': str(e)}), 500
    
@main.route('/getGroupDetails/<int:id>', methods=['GET'])
def groupDetail(id):
    print(id)
    try:
        with db.connection.cursor() as cursor:

            getDetail = """
            SELECT
                g.id,
                g.name as group_name,
                g.policy_id,
                p.name as policy,
                COUNT(a.id) as assets_quantity,
                os.name as operative_system
            FROM
                `group` g
                INNER JOIN policy p ON p.id = g.policy_id
                LEFT JOIN asset a ON a.group_id = g.id
                INNER JOIN operative_system os ON os.id = p.operative_system_id
            WHERE
                g.enabled = true
                AND g.id = %s
            LIMIT
                1;
            """

            getAssets = """
            SELECT
                a.id as `key`,
                a.*
            FROM
                asset a
            WHERE
                a.enabled = true
                AND a.group_id = %s
            """

            cursor.execute(getDetail, (id,))
            result = cursor.fetchall()
            data = {'assets': []}
            data['group'] = dataToJson(cursor.description, result)[0]

            if data['group']['assets_quantity'] > 0:
                cursor.execute(getAssets,(id,))
                result = cursor.fetchall()
                data['assets'] = dataToJson(cursor.description, result)

        return jsonify(data), 200

    
    except Exception as e:
        db.connection.rollback()
        return jsonify({'message': "Ocurrió un error inesperado", 'error': str(e)}), 500

@main.route('/getGroupById/<int:id>', methods=['GET'])
def getGroupById(id):
    cursor = db.connection.cursor()
    sql = f"""SELECT
        g.id as "key",
        g.id,
        g.name,
        g.policy_id
    FROM
        `group` g
        INNER JOIN policy p ON g.policy_id = p.id
        INNER JOIN operative_system os ON p.operative_system_id = os.id
    WHERE
         os.id = {id}
    ORDER by
        g.name ASC
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    data = dataToJson(cursor.description, result)
    return jsonify(data), 200