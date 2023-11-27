
#from src.database.db_mysql import db, dataToJson

data_test = [ 
    {'host' : '172.16.86.129', 'hostname':'ubuntudb', 'user' : 'dbadmin' ,'password':'root123', 'cert': '' },
    {'host' : '172.16.86.128', 'hostname':'windows 10', 'user' : 'admin' ,'password':'admin123', 'cert': '' },
    {'host' : '192.168.222.129', 'hostname':'ubuntu-server-1', 'user' : 'srvadmin' ,'password':'root123', 'cert': '' },
]



def get_credentials(host):
    """"Establecer conexion con base de datos o keyvault para obtener credenciales de host """
    for dv in data_test:
        if dv['host'] == host:
            return (dv['user'], dv['password'])
    return 0

def set_credentials (host, user, password):
    next

def update_credentials(host, user, password):
    next

def create_certificate(host):
    next


