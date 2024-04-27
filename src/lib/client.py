from socket import *
from lib.constants import BUFFER_SIZE
from lib.protocol import Protocol

class Client:
    def __init__(self, host, port, args):
        self.host = host
        self.port = port
        self.protocol = Protocol()

    def start(self):
        # Creamos el Socket
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        # Habria que crear el socket de transferencia, este es el de conexion
        message = ' '
        while message.upper() != 'FIN' :
            message = input("Input lowercase sentence:")
            self.upload(message, clientSocket)
            archivo_completo = self.download(clientSocket)
            print(archivo_completo.decode())

        # Cerramos
        clientSocket.close()

    def upload(self, archivo, socket):
        self.protocol.send(archivo, socket, self.host, self.port)
        return
    
    def download(self, socket):
        archivo_completo = self.protocol.receive(socket)
        return archivo_completo