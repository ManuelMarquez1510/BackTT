
#DOCUMENTACION DE LA CLASE


#Bibliotecas
import paramiko as pk
import src.services.pam_interface as pam
import socket
import os
import subprocess
# import pam_interface as pam

class connection: 

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.client = pk.client.SSHClient()
        #self.__set_connection()
        

    def set_connection (self): 
        self.client.set_missing_host_key_policy(pk.AutoAddPolicy())
        
        credentials = pam.get_credentials(self.host)
        #print (credentials)
        if credentials['status'] == 'OK':   
            credentials = credentials['data'][0]
            status =  self.stablish_connection(credentials) 
            del credentials
            return status
        else:
            self.client.close()
            return {'status': 'ERROR', 'msg': 'Credenciales no identificadas'}
    

    def close_connection (self):
        self.client.close()

    def send_command(self,comando):
        #print (f"COMMAND: {comando}")
        _stdin, _stdout,_stderr = self.client.exec_command(comando)
        #print ("STDOUT: ",_stdout.read().decode())
        #print ("STDERR: ", _stderr.read().decode())
        if _stderr is not None: 
            return (_stderr.read().decode().strip()) 
        else:
            return (_stdout.read().decode().strip()) 
    
    def get_evaluation_file (self, evaluation, filename): 
        sftp = self.client.open_sftp()

        path = os.path.join(".",evaluation)
        os.makedirs(path, exist_ok=True)

        sftp.get(filename,f"./{evaluation}/{filename}")
        sftp.close()

        self.send_command(f"rm {filename}")
    
    def stablish_connection(self,credentials): 
        try:
            # Connect to the server
            self.client.connect(self.host, username= credentials['user'], password= credentials['password'], port= self.port)
            print ('CONEXIÓN ESTABLECIDA')
            return {'status': 'OK', 'msg': 'conexión establecida'}
        except Exception as e:
            self.client.close()   
            return {f"status': 'ERROR', 'msg': '{e}"}
        finally:
            del credentials


    @staticmethod
    def check_connection(host, user, password, port):
        client = pk.client.SSHClient()
        client.set_missing_host_key_policy(pk.AutoAddPolicy())
        status = 0
        hostname = ''
        try:
            
            client.connect(host, port, user, password)
            print("Conexion realizada con exito")
            _stdin, _stdout,_stderr = client.exec_command('hostname')
            hostname =_stdout.read().decode()
            status = 1 

        except Exception as e:
            print(f"Error: {e}")
               
        finally:
            client.close()

        return (status,hostname)

    @staticmethod
    def check_host_port(host, port):
        print (f'testing with {host} and port {port}')
        try:
            socket.create_connection((host, port), timeout=5)
            status = 1
            #print (f"El host {host} en el puerto {port} está activo.")
        except (socket.timeout, socket.error):
            #print (f"El host {host} en el puerto {port} no está activo.")
            status = 0
        return status


    @staticmethod
    def check_ping(host):
        try:
            # Ejecuta el comando ping en el sistema
            print ('Validando ping')
            result = subprocess.run(["ping", "-c", "4", host], capture_output=True, text=True, timeout=10)

            # Verifica el código de salida del comando ping
            if result.returncode == 0:
                print(f"El host {host} responde al ping.")
            else:
                print(f"El host {host} no responde al ping.")
                print(result.stderr)  # Imprime información adicional del comando ping en caso de error

        except subprocess.TimeoutExpired:
            print(f"Se agotó el tiempo de espera para el ping al host {host}.")





    """ METODOS EXPUESTOS AL INTERNAL API """
    @staticmethod
    def init_connection (host, user, password, port):
        #Verificar estado del puerto con el host
        if not connection.check_host_port (host, port): 
            return {'message' : f'Puerto o host no esta habilitado', 'Error': 1} 
        
        result_tuple = connection.check_connection (host, user, password, port)
        hostname = result_tuple[1]
        if not result_tuple[0]:
            return {'message' : f'Credenciales no validas', 'Error': 1} 
        
        pam.set_credentials(host, user, password)

        return {'message' : f'Conexión exitosa con {hostname}', 'Error': 0}

        

