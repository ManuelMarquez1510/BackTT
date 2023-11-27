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


def evaluate_policy (): 
    next


def evaluate_host (host):
    return evaluation.evaluate_host(host)
