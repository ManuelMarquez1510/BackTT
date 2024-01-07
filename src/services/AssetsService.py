from src.database.db_mysql import db, dataToJson

def get_assets_by_group(id_group):
    try:
        with db.connection.cursor() as cursor:

            getAssets = """
            SELECT
                a.name,
                a.host,
                a.port,
                os.name as os,
                g.name as `group`,
                ac.user,
                ac.password,
                g.policy_id
            FROM
                asset a
                inner join operative_system os on os.id = a.operative_system_id
                inner join `group` g on g.id = a.group_id
                inner join asset_credentials ac on ac.host = a.host
            WHERE
                a.enabled = true
                AND a.group_id = %s
            """
            
            cursor.execute(getAssets,(id_group,))
            result = cursor.fetchall()
            data = dataToJson(cursor.description, result)

        return data

    except Exception as e:
        db.connection.rollback()
        return [{'message': "Ocurrió un error inesperado", 'Error': 1, 'err_description': str(e)}]
    
def get_assets_by_id(id_asset):
    try:
        with db.connection.cursor() as cursor:

            getAssets = """
            SELECT
                a.name,
                a.host,
                a.port,
                os.name as os,
                g.name as `group`,
                ac.user,
                ac.password,
                g.policy_id
            FROM
                asset a
                inner join operative_system os on os.id = a.operative_system_id
                inner join `group` g on g.id = a.group_id
                inner join asset_credentials ac on ac.host = a.host
            WHERE
                a.enabled = true
                AND a.id = %s
            """
            
            cursor.execute(getAssets,(id_asset,))
            result = cursor.fetchall()
            data = dataToJson(cursor.description, result)

        return data

    except Exception as e:
        db.connection.rollback()
        return [{'message': "Ocurrió un error inesperado", 'Error': 1, 'err_description': str(e)}]