from socket import *
from lib.constants import BUFFER_SIZE
from lib.protocol import Protocol
from lib.file_manager import *
from lib.file_manager import *

class Client:
    def __init__(self, host, port, args):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.protocol = Protocol()

    def start(self):
        # Creamos el Socket
        #clientSocket = socket(AF_INET, SOCK_DGRAM)
        # Habria que crear el socket de transferencia, este es el de conexion
        #message = ' '
        #while message.upper() != 'FIN' :
        #    message = input("Input lowercase sentence:")
        #    self.upload(message, clientSocket)
        #    complete_file = self.download(clientSocket)
        #    print(complete_file.decode())

        # Cerramos
        #clientSocket.close()
        return

    def upload(self, file_path):
        file_manager = FileManager()
        file_content = file_manager.read_file_bytes(file_path)
        self.protocol.send(file_content, self.socket, self.host, self.port)
        return
    
    def download(self):
        complete_file = self.protocol.receive(socket)
        return complete_file
    
    def close_socket():
        socket.close()