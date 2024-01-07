from src.database.db_mysql import db, dataToJson
import json

def get_rules(policy_id):
    try:
        with db.connection.cursor() as cursor:

            getRules = """
            SELECT
                r.title,
                r.rule_id,
                r.severity,
                r.cvss,
                r.description,
                r.tests

            FROM
                policy_rule pr
                inner join rule r on r.id = pr.rule_id
            WHERE
                pr.policy_id = %s
            """
            
            cursor.execute(getRules,(policy_id,))
            result = cursor.fetchall()
            data = dataToJson(cursor.description, result)

            for rule in data: 
                tests = json.loads(rule['tests'])
                rule['tests'] = tests
        return data

    except Exception as e:
        db.connection.rollback()
        return [{'message': "Ocurrió un error inesperado", 'Error': 1, 'err_description': str(e)}]

def get_policy (policy_id): 
    try:
        with db.connection.cursor() as cursor:

            getPolicy = """SELECT id, name, description FROM policy WHERE id = %s """
            
            cursor.execute(getPolicy,(policy_id,))
            result = cursor.fetchall()
            data = dataToJson(cursor.description, result)

        return data

    except Exception as e:
        db.connection.rollback()
        return [{'message': "Ocurrió un error inesperado", 'Error': 1, 'err_description': str(e)}]
