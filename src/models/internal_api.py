"""
INTERNAL API

API para comunicar modulos del servidor y servicios de backend con modulos de SCAP 

Documentar cada API con 
-Nombre.
-Descripcion
-Parametros obligatorios con tipos de datos
-Perametros opcionales con valores por defecto
-Resultado esperado
"""

#Modulos requeridos
import evaluation
import connection
from src.services.AssetsService import get_assets_by_group, get_assets_by_id



"""MODULOS DE CONEXION CON LOS DISPOSITIVOS"""


"""
    CONEXION INICIAL CON EL DISPOSITIVO
    

"""

""" 
Respuesta
 { 'message' : *********** ,
    'error' : 1|0    
}
"""
def init_connection (host, user, password):
    #return {'message' : f'OK', 'Error': '0'}
    return connection.connection.init_connection(host, user, password)

def get_assets_by_group(group_id):
    #return [{"group": "", "host": "", "name": "", "os": "", "password": "", "user": ""}, {...}, {...}, ...]
    #return in error [{'message': '', 'Error': 1, 'err_description': ''}]
    return get_assets_by_group(group_id)

def get_assets_by_id(id_asset):
    #return [{"group": "", "host": "", "name": "", "os": "", "password": "", "user": ""}]
    #return in error [{'message': '', 'Error': 1, 'err_description': ''}]
    return get_assets_by_id(id_asset)

def evaluate_policy (): 
    next


def evaluate_host (host):
    return evaluation.evaluate_host(host)
