

from datetime import datetime
import src.models.connection as connection
import src.models.validate_test as test_helper
#from src.models.internal_api import get_assets_by_group, get_assets_by_id
# from connection import connection
from src.services.scap_database_service import get_rules, get_policy
import hashlib

class evaluation: 

    def __init__ (self, name, policy, assets, rules) -> None: 
        self.name = name
        self.policy = policy
        self.rules = rules
        self.date = None
        self.time = None
        self.assets = assets
        self.result = {}


    def evaluate_policy (self): 
        date_time = datetime.now()
        self.date = date_time.strftime("%d-%m-%y")
        self.time = date_time.strftime("%H:%M:%S")
        
        rules_id = []
        for rule in self.rules: 
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
            'policy_status': 'PASS',
            'policy_avg': 100,
            'assets' : asset_ip,
            'rule_set' : rules_id
            }

        for asset in self.assets:
            #print (asset)
            as_connetion = connection.connection(asset['host'], asset['port'])
            connetion_status = as_connetion.set_connection()
            if connetion_status['status'] == 'OK':                 
                print ('INICIA EVALUACIÓN')
                print (f"Evaluated asset {asset}")
                rule_counter = 0
                total_rules = len (self.rules)

                host_result = {}

                for rule in self.rules: #Tests
                    rule_counter = rule_counter+1
                    print (f'Evaluation {rule_counter}/{total_rules} : {rule["rule_id"]} ')
                    test_array_aux = []
                    for test in rule["tests"]:
                        array_aux = []
                        for command in test['tests_dictionary']:
                            result = as_connetion.send_command(f"{command['test']}")
                            print (f"\tRegla {rule['rule_id']} comando enviado {command['test']}")
                            print (f"\tRespuesta obtenida: {result}")
                            array_aux.append(result)
                        test_array_aux.append(array_aux)
                    host_result[rule["rule_id"]] = test_array_aux
                as_connetion.close_connection()
                print ('CONEXION CERRADA')
                result_string = str(host_result)
                result_hash=hashlib.sha256(result_string.encode('utf-8')).hexdigest()
                
                evaluation_result[f'{asset["host"]}'] = {'hash_result': result_hash, 'dict_result': host_result, 'status': 'PASS', 'avg': 0 , 'done': "YES"}

            else :  
                print (f"Activo no disponible: {asset}")
                evaluation_result[f'{asset["host"]}'] = {'hash_result': "", 'dict_result': "", 'status': 'FAIL', 'avg': 0, 'done' : "NO" }
        
        self.result = evaluation_result

        self.evaluate_result()
        
        return {'status' : 'OK', 'data': evaluation_result }
        




    def evaluate_result (self): 
        #windows_list = ['Windows Server', 'Windows 10']
        #type_os = self.policy['OS']

        #if type_os.upper() in [item.upper() for item in windows_list]:
        #    print ('Windows policy')
        #else:
        print ('Evlaluacion politica: Linux')
        hosts_fails = 0
        for asset in self.result['assets']:
            if  self.result[asset]["done"] == "YES":
                asset_result = self.result[asset]['dict_result']
                asset_validation = self.validate_rules (asset_result)
                self.result[asset]['validation_result'] = asset_validation
                self.result[asset]['status'] = asset_validation['status']
                self.result[asset]['avg'] = asset_validation['avg']
                self.result[asset]['completed'] = asset_validation['pass']
                if asset_validation['status'] == "FAIL": 
                    hosts_fails = hosts_fails + 1
            else : 
                self.result[asset]['validation_result'] = {}
                self.result[asset]['status'] = "FAIL"
                self.result[asset]['avg'] = 0
                self.result[asset]['completed'] = 0
                hosts_fails = hosts_fails + 1

        if hosts_fails > 0: 
            self.result['policy_status'] = 'FAIL' 
        num_activos = len(self.result['assets'])
        self.result['policy_avg'] = round( 100 - (hosts_fails*100)/num_activos, 2)
        self.result['policy_completed'] = num_activos - hosts_fails



    def validate_rules (self, asset_results):
        validation_result = []
        rule_pass_count = 0
        num_rules = len(self.rules)
        asset_status = "FAIL"
        for rule in self.rules:
            evaluation_result = asset_results[rule['rule_id']]
            test_count = 0
            rule_status = "FAIL"
            total_proof = 0
            fails = 0
            pass_s = 0
            for test in rule['tests']:
                test_type = test['test_type']
                comment = test['test_comment']
                proof_counts = 0
                for proof in test['tests_dictionary']: 
                    result = False
                    if test_type == 'dpkginfo_test': 
                        #print (rule)
                        result = test_helper.dpkginfo_test (evaluation_result[test_count][proof_counts], comment)
                    
                    if result:
                        pass_s = pass_s+1
                    else :
                        fails = fails+1 
                    
                    total_proof = total_proof+1
                    proof_counts= proof_counts +1
                test_count = test_count + 1
            
            if fails == 0: 
                rule_status = "PASS"
                rule_pass_count = rule_pass_count + 1 
        
            validation_result.append({"rule_id": rule['rule_id'], "rule_status": rule_status, "pass" : pass_s, "fail": fails, "tp": total_proof })

        if num_rules - rule_pass_count == 0:
            asset_status = "PASS"
        avg = round((rule_pass_count*100)/num_rules, 2)

        return {"status" : asset_status, "avg": avg, "pass": rule_pass_count,"detailed_result" : validation_result}



    def evaluate_windows_policy (self):
        print ("Evaluación de politica windows")
    

    def evaluate_linux_policy (self):
        count = 0
        for rule in self.rules:
            rule_test = rule['test']
            rule_test_comment = rule['comment']
            rule_test_type = rule['test_type']

            #print (f"\nrule: {rule['rule_id']}-{rule_test_comment}")
            rule_validation_condition = 1 
            if rule_test_type == 'dpkginfo_test': 
                self.dpkginfo_test(rule_test_comment,count)

            count= count + 1            

@staticmethod
def print_evaluation_result (result):
    assets = result['data']['assets']
    result_str = f"""
    Nombre de evaluacion: {result['data']['name']}
    Politica evaluada: {result['data']['policy']}
    Fecha: {result['data']['date']} hora: {result['data']['time']}
    Activos evaluados: {" ".join(map(str, assets))}
    Estatus de la evaluación: {result['data']['policy_status']} - {result['data']['policy_avg']}% host
    Resultados: """
    print (result_str)

    for asset in assets: 
        print (f"\tActivo: {asset}")
        print (f"\tHash: {result['data'][asset]['hash_result']}")
        print (f"\tEvaluado: {result['data'][asset]['done']}")
        if not (result['data'][asset]['validation_result'] == {}): 
            print (f"\tEstatus: {result['data'][asset]['status']} - {result['data'][asset]['validation_result']['pass']}/{len(result['data']['rule_set'])} : {result['data'][asset]['avg']}% de cumplimiento")
        
            for rule in result['data'][asset]['validation_result']['detailed_result']:
                print (f"\t\tRegla: {rule['rule_id']} : {rule['rule_status']} {rule['pass']}/{rule['tp']}")
        
            

def format_response (assets, result): 
    assets_completed = result ['data']['policy_completed']
    assets_array = []

    for asset in assets: 
        if result['data'][asset["host"]]['validation_result'] == {}: 
            comp = 0
            err = True
        else : 
            comp = result['data'][asset["host"]]['validation_result']['pass']
            err = False
        asset_format = {
        "group": asset["group"], 
        "host": asset["host"],
        "name": asset["name"],
        "os": asset["os"],
        "completed": comp,
        "error" : err
        }
        assets_array.append(asset_format)
    
    return {"assets_completed": assets_completed, "assets": assets_array}
    

    
    
""" METODOS EXPUESTOS AL INTERNAL API """
@staticmethod
def evaluate_assets (assets): 

    print (assets)
    #print (assets)
    if not len(assets): 
        return "{'status': 'ERROR', 'msg': 'No se encontraron activos'}"
    
    policy = get_policy(assets[0]["policy_id"])[0]
    rules = get_rules(assets[0]["policy_id"])


    evl = evaluation(f"evaluacion {policy['name']}", policy, assets, rules=rules )
    result = evl.evaluate_policy()
    #print ( result['data']['192.168.222.129'])
    print_evaluation_result(result)

    response = format_response(assets, result)
    print (response)
    #return result
    return response


""" METODOS DE PRUEBA ELIMINAR AL PONER EN PRODUCCION Y HACER REFERENCIAS CORRESPONDIENTES """ 




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
        'evaluation_result': [FAIL(1/3), PASS, FAIL],
        'status': 'FAIL|PASS',
        'avg': 33.3%
    }
    '192.168.3.xx' : {
        'hash_result': 
    }
    }}


    assets_completed: 1, 
    date : 
    time : 
    assets: [
      {
        group: 'Default Ubuntu',
        host: 'scaptooldev.ddns.net',
        name: 'LuisMiguel',
        os: 'Ubuntu 20.0.4 LTS',
        password: 'root123',
        user: 'dbadmin',
        completed: 3,
        error: true|false
      },
      {
        group: 'Default Ubuntu',
        host: 'manuel-scap.eastus.cloudapp.azure.com',
        name: 'ManuelMarquez',
        os: 'Ubuntu 20.0.4 LTS',
        password: 'BurroBlanco123',
        user: 'dbmanuel',
        completed: 1,
      },

 """
