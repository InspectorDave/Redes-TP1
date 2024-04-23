from socket import *

class Client:
    def __init__(self, host, port, args):
        self.host = host
        self.port = port

    def start(self):
        # Creamos el Socket
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        message = ' '
        while message.upper() != 'FIN' :
            message = input("Input lowercase sentence:")

            # Enviamos directamente, no hay handshaking
            clientSocket.sendto(message.encode(),(self.host, self.port))
            # Recibimos la modificacion
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

            print(modifiedMessage.decode())

        # Cerramos
        clientSocket.close()