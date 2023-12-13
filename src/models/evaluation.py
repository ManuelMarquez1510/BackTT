

from datetime import datetime
import src.models.connection as connection
#from src.models.internal_api import get_assets_by_group, get_assets_by_id
# from connection import connection
import hashlib

class evaluation: 

    def __init__ (self, name, policy, assets) -> None: 
        self.name = name
        self.policy = policy
        self.date = None
        self.time = None
        self.assets = assets
        self.result = {}


    def evaluate_policy (self): 
        date_time = datetime.now()
        self.date = date_time.strftime("%d-%m-%y")
        self.time = date_time.strftime("%H:%M:%S")
        
        rules_id = []
        for rule in self.policy['benchmark']: 
            rules_id.append (rule['rule_id'])
        
        asset_name= []
        asset_ip = []
        for asset in self.assets:
            #asset_name.append(asset['hostname'])
            asset_ip.append(asset['host'])
    

        evaluation_result = {
            'name' : self.name,
            'policy' : self.policy['name'],
            'date' : self.date,
            'time' : self.time,
            'assets' : {'host': asset_ip},
            'rules_id' : rules_id
            }

        for asset in self.assets:
            print (asset)
            as_connetion = connection.connection(asset['host'], asset['port'])
            connetion_status = as_connetion.set_connection()
            if connetion_status['status'] == 'ERROR': 
                return as_connetion
            result_array =[]
            result_string=''
            print ('INICIA EVALUACIÓN')
            for rule in self.policy['benchmark']:
                result = as_connetion.send_command(f"{rule['test']}")
                result_array.append(result)
                result_string = result_string + f"{result},"
            as_connetion.close_connection()
            print ('CONEXION CERRADA')
            result_hash=hashlib.sha256(result_string.encode('utf-8')).hexdigest()
            
            evaluation_result[f'{asset["host"]}'] = {'hash_result': result_hash, 'string_result' : result_string, 'array_result': result_array}

        self.result = evaluation_result

        #evaluation.evaluate_result()
        
        return {'status' : 'OK', 'data': evaluation_result }
        

    def evaluate_result (self): 
        windows_list = ['Windows Server', 'Windows 10']
        type_os = self.policy['OS']

        if type_os.upper() in [item.upper() for item in windows_list]:
            print ('Windows policy')
        else:
            print ('linux policy')
            evaluation.evaluate_linux_policy()
        print('Evaluation')


    def evaluate_windows_policy (self):
        print ("Evaluación de politica windows")
    

    def evaluate_linux_policy (self):
        print ("Evaluación de politica windows")




    
""" METODOS EXPUESTOS AL INTERNAL API """
@staticmethod
def evaluate_assets (assets): 

    print (assets)
    if not len(assets): 
        return "{'status': 'ERROR', 'msg': 'No se encontraron activos'}"
    
    policy = get_policy()

    evl = evaluation("evaluacion prueba", policy, assets)
    result = evl.evaluate_policy()
    print (result)
    return result


""" METODOS DE PRUEBA ELIMINAR AL PONER EN PRODUCCION Y HACER REFERENCIAS CORRESPONDIENTES """

def get_policy():
  policy = {
    'policy_id': '00001', 
    'name':'Politica des pruebas',
    'OS' : 'Ubuntu Server',
    'OS_version': '22.04 LTS',
    'benchmark': [
        {
            'rule_id': "RP001",
            'Name': "Nombre de la regla",
            'Description': 'Regla de prueba para validar funcionamiento',
            'test': 'dpkg -l | grep telnetd',
            'type_of_finding': '',
            'finding': '',
            'severity': 'low',
            'filepath': '',
            'pattern' : ''
        },
        {
            'rule_id': "RP002",
            'Name': "Nombre de la regla",
            'Description': 'Regla de prueba para validar funcionamiento',
            'test': 'dpkg -l | grep rsh-server',
            'type_of_finding': '',
            'finding': '',
            'severity': 'low',
            'filepath': '',
            'pattern' : ''
        },
        {
            'rule_id': "RP003",
            'Name': "Nombre de la regla",
            'Description': 'Regla de prueba para validar funcionamiento',
            'test': 'dpkg -l | grep ufw',
            'type_of_finding': 'dpkginfo',
            'finding': 'package ufw is installed',
            'severity': 'low',
            'filepath': '',
            'pattern' : ''
        },
        {
            'rule_id': "RP004",
            'Name': "Nombre de la regla",
            'Description': 'Regla de prueba para validar funcionamiento',
            'test': 'dpkg -l | grep aide',
            'type_of_finding': 'dpkginfo',
            'finding': 'package aide is installed',
            'severity': 'low',
            'filepath': '',
            'pattern' : ''
        },
        {
            'rule_id': "RP005",
            'Name': "Nombre de la regla",
            'Description': 'Regla de prueba para validar funcionamiento',
            'test': 'dpkg -l | grep rsyslog',
            'type_of_finding': 'dpkginfo_object',
            'finding': 'package rsyslgo is installed',
            'severity': 'low',
            'filepath': '',
            'pattern' : ''
        }
        ]  
    }
  return policy    

