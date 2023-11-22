

from datetime import datetime
from connection import connection
import hashlib


#TESTING
import main_test

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
        policy_evaluation_name = f"{self.policy}_{self.date}"
        
        rules_id = []
        for rule in self.policy['benchmark']: 
            rules_id.append (rule['rule_id'])
        
        asset_name= []
        asset_ip = []
        for asset in self.assets:
            asset_name.append(asset['hostname'])
            asset_ip.append(asset['host'])
    

        evaluation_result = {
            'name' : self.name,
            'policy' : self.policy['name'],
            'date' : self.date,
            'time' : self.time,
            'assets' : {'hostnames' : asset_name, 'host': asset_ip},
            'rules_id' : rules_id
            }

        for asset in self.assets:

            as_connetion = connection(asset['host'])
            result_array =[]
            result_string=''
            for rule in self.policy['benchmark']:
                result = as_connetion.send_command(f"{rule['test']}")
                result_array.append(result)
                result_string = result_string + f"{result},"
            as_connetion.close_connection()
            
            result_hash=hashlib.sha256(result_string.encode('utf-8')).hexdigest()
            
            evaluation_result[f'{asset["hostname"]}'] = {'hash_result': result_hash, 'string_result' : result_string, 'array_result': result_array}

        self.result = evaluation_result

        evaluation.evaluate_result()
        
        return (evaluation_result)
    

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
        next
    

    def evaluate_linux_policy (self):
        next




    
""" METODOS EXPUESTOS AL INTERNAL API """

def evaluate_host (host): 

    policy = main_test.get_policy()
    test = evaluation("evaluacion prueba", policy, [host])
    result = test.evaluate_policy()
    print (result)
    return result







        

