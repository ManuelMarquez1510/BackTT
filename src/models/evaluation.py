

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
        for rule in self.policy['rule_set']: 
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
            'assets' : asset_ip,
            'rule_set' : rules_id
            }

        for asset in self.assets:
            #print (asset)
            as_connetion = connection.connection(asset['host'], asset['port'])
            connetion_status = as_connetion.set_connection()
            if connetion_status['status'] == 'ERROR': 
                return as_connetion
            result_array =[]
            result_string=''
            print ('INICIA EVALUACIÓN')
            for rule in self.policy['rule_set']:
                result = as_connetion.send_command(f"{rule['test']}")
                result_array.append(result)
                result_string = result_string + f"{result},"
            as_connetion.close_connection()
            print ('CONEXION CERRADA')
            result_hash=hashlib.sha256(result_string.encode('utf-8')).hexdigest()
            
            evaluation_result[f'{asset["host"]}'] = {'hash_result': result_hash, 'string_result' : result_string, 'array_result': result_array,'evaluation_result': [], 'status': 'PASS', 'avg': 0 }

        self.result = evaluation_result

        self.evaluate_result()
        
        return {'status' : 'OK', 'data': evaluation_result }
        

    def evaluate_result (self): 
        windows_list = ['Windows Server', 'Windows 10']
        type_os = self.policy['OS']

        if type_os.upper() in [item.upper() for item in windows_list]:
            print ('Windows policy')
        else:
            print ('Evlaluacion politica: Linux')
            self.evaluate_linux_policy()
        
        num_rules = len(self.policy['rule_set'])
        for asset in self.assets: 
            num_fails = (self.result[asset]['evaluation_result']).count('FAIL')
            self.result[asset]['avg'] = 100 - (num_fails*100)/num_rules
            if num_fails > 0:  
                self.result[asset]['status'] = 'FAIL'


        avg = len(self.policy['assets'])




    def evaluate_windows_policy (self):
        print ("Evaluación de politica windows")
    

    def evaluate_linux_policy (self):
        count = 0
        for rule in self.policy['rule_set']:
            rule_test = rule['test']
            rule_test_comment = rule['comment']
            rule_test_type = rule['test_type']

            #print (f"\nrule: {rule['rule_id']}-{rule_test_comment}")
            rule_validation_condition = 1 
            if rule_test_type == 'dpkginfo_test': 
                self.dpkginfo_test(rule_test_comment,count)

            count= count + 1
        

    def dpkginfo_test(self,rule_test_comment,count):
        rule_validation_condition = 1
        if 'is not installed' in rule_test_comment :
            rule_validation_condition = 0
        for asset in self.assets:
            asset_result = self.result[asset['host']]['array_result'][count]
            is_in_result = 1
            if asset_result == '': 
                is_in_result =0
            
            if rule_validation_condition and is_in_result: 
                self.result[asset['host']]['evaluation_result'].append('PASS')
                #print (f"asset: {asset['host']} rule: {rule['rule_id']}-{rule_test_comment} STATUS: PASS")
                #print (f"asset: {asset['host']} result: {asset_result} status: PASS")
            elif not rule_validation_condition and not is_in_result: 
                self.result[asset['host']]['evaluation_result'].append('PASS')
                #print (f"asset: {asset['host']} rule: {rule['rule_id']}-{rule_test_comment} STATUS: PASS")
                #print (f"asset: {asset['host']} result: {asset_result} status: PASS")
            else: 
                self.result[asset['host']]['evaluation_result'].append('FAIL')
                #print (f"asset: {asset['host']} rule: {rule['rule_id']}-{rule_test_comment} STATUS: FAIL")
                #print (f"asset: {asset['host']} result: {asset_result} status: FAIL")


                

@staticmethod
def print_evaluation_result (result):
    assets = result['data']['assets']
    print (f"""
    Nombre de evaluacion: {result['data']['name']}
    Politica evaluada: {result['data']['policy']}
    Fecha: {result['data']['date']} hora: {result['data']['time']}
    Activos evaluados: {" ".join(map(str, assets))}
    Resultados: """)
    for asset in assets: 
        print (f"\tActivo: {asset}")
        print (f"\tHash: {result['data'][asset]['hash_result']}")
        print (f"\tEstatus: {result['data'][asset]['status']} - {result['data'][asset]['avg']}% de cumplimiento")
        for index in range (len( result['data']['rule_set'])):
            print (f"\tRule id: {result['data']['rule_set'][index]} - {result['data'][asset]['evaluation_result'][index]}")
    
    
    
""" METODOS EXPUESTOS AL INTERNAL API """
@staticmethod
def evaluate_assets (assets): 

    #print (assets)
    if not len(assets): 
        return "{'status': 'ERROR', 'msg': 'No se encontraron activos'}"
    
    policy = get_policy()

    evl = evaluation("evaluacion prueba", policy, assets)
    result = evl.evaluate_policy()
    print ( result)
    print_evaluation_result(result)
    return result


""" METODOS DE PRUEBA ELIMINAR AL PONER EN PRODUCCION Y HACER REFERENCIAS CORRESPONDIENTES """

def get_policy():
  policy = {
    'policy_id': '00001', 
    'name':'Canonical Ubuntu 20.04 LTS STIG SCAP Benchmark',
    'description': 'This Security Technical Implementation Guide is published as a tool to improve the security of Department of Defense (DOD) information systems. The requirements are derived from the National Institute of Standards and Technology (NIST) 800-53 and related documents. Comments or proposed revisions to this document should be sent via email to the following address: disa.stig_spt@mail.mil.',
    'OS' : 'Ubuntu 20.04 LTS',
    'rule_set': [
        {
            'rule_id': "238200",
            'title': "The Ubuntu operating system must allow users to directly initiate a session lock for all connection types.",
            'severity': "medium", 
            'weight' : 10.0,
            'description': 'A session lock is a temporary action taken when a user stops work and moves away from the immediate physical vicinity of the information system but does not want to log out because of the temporary nature of the absence. The session lock is implemented at the point where session activity can be determined. Rather than be forced to wait for a period of time to expire before the user session can be locked, the Ubuntu operating systems need to provide users with the ability to manually invoke a session lock so users may secure their session if they need to temporarily vacate the immediate physical vicinity. Satisfies: SRG-OS-000030-GPOS-00011, SRG-OS-000031-GPOS-00012',
            'fix_text': 'Rule fix_text: Install the "vlock" package (if it is not already installed) by running the following command: $ sudo apt-get install vlock',
            'test_type': 'dpkginfo_test', 
            'test': 'dpkg -l | grep vlock',
            'comment': 'package vlock is installed'
        },
        {
            'rule_id': "238326",
            'title': "The Ubuntu operating system must not have the telnet package installed.",
            'severity': "high", 
            'weight' : 10.0,
            'description': 'Passwords need to be protected at all times, and encryption is the standard method for protecting passwords. If passwords are not encrypted, they can be plainly read (i.e., clear text) and easily compromised.',
            'fix_text': 'Remove the telnet package from the Ubuntu operating system by running the following command: $ sudo apt-get remove telnetd',
            'test_type': 'dpkginfo_test', 
            'test': 'dpkg -l | grep telnetd',
            'comment': 'package telnetd is not installed'
        },{
            'rule_id': "238327",
            'title': "The Ubuntu operating system must not have the rsh-server package installed.",
            'severity': "high", 
            'weight' : 10.0,
            'description': 't is detrimental for operating systems to provide, or install by default, functionality exceeding requirements or mission objectives. These unnecessary capabilities or services are often overlooked and therefore may remain unsecured. They increase the risk to the platform by providing additional attack vectors. Operating systems are capable of providing a wide variety of functions and services. Some of the functions and services, provided by default, may not be necessary to support essential organizational operations (e.g., key missions, functions). Examples of non-essential capabilities include, but are not limited to, games, software packages, tools, and demonstration software, not related to requirements or providing a wide array of functionality not required for every mission, but which cannot be disabled.',
            'fix_text': 'Configure the Ubuntu operating system to disable non-essential capabilities by removing the rsh-server package from the system with the following command: $ sudo apt-get remove rsh-server',
            'test_type': 'dpkginfo_test', 
            'test': 'dpkg -l | grep rsh-server',
            'comment': 'package rsh-server is not installed'
        }
        ]  
    }
  return policy    




""" 
'data': {
    'name': 'evaluacion prueba', 
    'policy': 'Canonical Ubuntu 20.04 LTS STIG SCAP Benchmark', 
    'date': '26-12-23', 'time': '16:15:48', 
    'assets': {'host': ['192.168.3.55']}, 
    'rules_id': ['238200', '238326', '238327'], 
    'policy_status' : PASS|FAIL,
    'policy_avg' : 0 
    '192.168.3.55': {
        'hash_result': 'b0f8fd8fd26179f77e373926e21ae518fd359eb90a47f4d5d63efcaec105d901', 
        'string_result': 'ii  vlock                                 2.2.2-8                           amd64        Virtual Console locking program\n,ii  telnetd                               0.17-41.2build1                   amd64        basic telnet server\n,,',
        'array_result': ['ii  vlock                                 2.2.2-8                           amd64        Virtual Console locking program\n', 'ii  telnetd                               0.17-41.2build1                   amd64        basic telnet server\n', ''],
        'evaluation_result': [],
        'status': 'FAIL',
        'avg': 0
    }
    '192.168.3.xx' : {
        'hash_result': 
    }
    }}




 """
