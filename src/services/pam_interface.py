
from src.database.db_mysql import db, dataToJson


data_test = [ 
    {'host' : '172.16.86.129', 'hostname':'ubuntudb', 'user' : 'dbadmin' ,'password':'root123', 'cert': '' },
    {'host' : '172.16.86.128', 'hostname':'windows 10', 'user' : 'admin' ,'password':'admin123', 'cert': '' }
]



def get_credentials(host):
    """"Establecer conexion con base de datos o keyvault para obtener credenciales de host """
    try:
        with db.connection.cursor() as cursor:

            getAssets = """
            SELECT
                ac.host,
                ac.user,
                ac.password
            FROM
                asset_credentials ac
            WHERE
                ac.host = %s
            """
            
            cursor.execute(getAssets,(host,))
            result = cursor.fetchall()
            data = dataToJson(cursor.description, result)

        return {'status' : 'OK', 'data': data}

    except Exception as e:
        db.connection.rollback()
        return {'message': "Ocurrió un error inesperado", 'Error': 1, 'err_description': str(e)}


def set_credentials(host, user, password): 
    cursor = db.connection.cursor()
    sqlUser = f"""
        INSERT INTO asset_credentials (user, password, host)
        VALUES 
        (
            "{user}",
            "{password}",
            "{host}"
        )
        """
    result = 0
    try:
        cursor.execute(sqlUser)
        db.connection.commit()
        result = 1
    except Exception as e:
        db.connection.rollback()  # Revertir cambios en caso de error

    finally:
        cursor.close()
    
    return result



def update_credentials(host, user, password):
    next

def create_certificate(host):
    next


