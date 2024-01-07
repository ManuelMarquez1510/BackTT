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
    

def save_evaluation_result (assets, result, policy_id) : 
    #print ("Save into DB ", assets)
    result = result['data']
    #print (result)
    cursor = db.connection.cursor()
    try:
        cursor.execute("START TRANSACTION")
        #print ("TRY")
        for asset_aux in assets: 
            asset = asset_aux['host']
            aux_result = {}
            if not (result[asset]['validation_result'] == {}):
                for rule in result[asset]['validation_result']['detailed_result']:
                    aux_result[rule['rule_id']] = True if rule['rule_status'] == "PASS" else False
                
                pass_num = result[asset]['validation_result']['pass']

            else : 
                pass_num = 0 
            #print (f"ASSET ID {asset_aux['asset_id']}")
            #print (f"PoC {result[asset]['avg']}")
            #print (pass_num)

            insert_query = "INSERT INTO diagnosis (asset_id, percentage_of_compliance, completed, result, ext_data, policy_id ) VALUES (%s, %s, %s, %s, %s, %s)"
            
            data_to_insert = (
                asset_aux['asset_id'],
                result[asset]['avg'],
                pass_num,
                json.dumps(aux_result),
                json.dumps(result[asset]["validation_result"]),
                policy_id
            )
            cursor.execute(insert_query, data_to_insert)
        db.connection.commit()
        print ("Resultado guardado en BD")
    except Exception as e:
        print (f"Exeption {e}")
        db.connection.rollback()  # Revertir cambios en caso de error

    finally:
        cursor.close()

        