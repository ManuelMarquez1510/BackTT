
import internal_api as api



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
    }, 
    {
        'hostname': 'ubuntu-server-1',
        'host': '192.168.222.129', 
        'OS': 'Ubuntu Server'
    }
]


print('Pruebas de integración del API interno')

status = api.init_connection(assets[2]['host'],'srvadmin','root123')
print (status)

if status['Error']: 
    print (status['message'])
else: 
    evaluation = api.evaluate_host(assets[2]['host'])
    print (evaluation)
