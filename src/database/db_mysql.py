from flask_mysqldb import MySQL
db = MySQL()

def dataToJson(cursor_description, data):
    insertObject = []
    keys = [val[0] for val in cursor_description]
    for record in data:
        insertObject.append(dict(zip(keys,record)))
    return insertObject