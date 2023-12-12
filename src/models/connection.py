
#DOCUMENTACION DE LA CLASE


#Bibliotecas
import paramiko as pk
#import src.services.pam_interface as pam
import socket
import os
import subprocess
import pam_interface as pam

class connection: 

    def __init__(self, host) -> None:
        self.host = host
        self.client = pk.client.SSHClient()
        self.__set_connection()
        

    def __set_connection (self): 
        self.client.set_missing_host_key_policy(pk.AutoAddPolicy())
        credentials = pam.get_credentials(self.host)
        if isinstance (credentials, tuple):   
            self.client.connect(self.host, username= credentials[0], password= credentials[1])
            del credentials
        else:
            """LOG: CREDENCIALES NO IDENTIFICADAS """
            print("Credenciales no identificadas")
            self.client.close()
            return 0
    

    def close_connection (self):
        self.client.close()

    def send_command(self,comando):
        #_stdin, _stdout,_stderr = self.client.exec_command("dpkg -l | grep ftp")
        _stdin, _stdout,_stderr = self.client.exec_command(comando)
        return (_stdout.read().decode()) 
    
    def get_evaluation_file (self, evaluation, filename): 
        sftp = self.client.open_sftp()

        #Pasarlo a un FS
        path = os.path.join(".",evaluation)
        os.makedirs(path, exist_ok=True)

        sftp.get(filename,f"./{evaluation}/{filename}")
        sftp.close()

        self.send_command(f"rm {filename}")
    

    @staticmethod
    def test_connection(host, port=22):
        client = pk.client.SSHClient()
        client.set_missing_host_key_policy(pk.AutoAddPolicy())
        credentials = pam.get_credentials(host)
        if isinstance (credentials, tuple):   
            try:
                # Connect to the server
                client.connect(host, port, credentials[0], password= credentials[1])
                print("Conexion realizada con exito")
                # Close the SSH connection
                client.close()

            except Exception as e:
                print(f"Error: {e}")
                client.close()    
            finally:
                del credentials
        
        else:
            """LOG: CREDENCIALES NO IDENTIFICADAS """
            print("Credenciales no identificadas")
            client.close()
            return 0


    @staticmethod
    def check_connection(host, user, password, port=22):
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
    def check_host_port(host, port=22):
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
        
        result_tuple = connection.check_connection (host, user, password)
        hostname = result_tuple[1]
        if not result_tuple[0]:
            return {'message' : f'Credenciales no validas', 'Error': 1} 
        
        pam.set_credentials(host, user, password)

        return {'message' : f'Conexión exitosa con {hostname}', 'Error': 0}

        


