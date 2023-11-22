
from connection import connection
from evaluation import evaluation

import internal_api


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


assets = [
    {
        'hostname': 'ubuntudb',
        'host': "172.16.86.129",
        'OS': "Ubuntu Server",
    },
    {
        'hostname': 'windows 10',
        'host': "172.16.86.128",
        'OS': "Windows 10",
    }
]

print('CODIGO PARA REALIZAR PRUEBAS')

test = evaluation("evaluacion prueba", policy, [assets[0]])
test.evaluate_policy()


connection.check_host(assets[1]['host'])

connection.test_connection(assets[1]['host'])


def get_policy(): 
    return policy

