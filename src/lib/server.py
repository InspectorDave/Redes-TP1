from socket import *
from threading import Thread
from threading import Lock

class Server:
    def __init__(self, host, port, args):
        self.host = host
        self.port = port
        return
    
    def start(self):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind((self.host, self.port))
        print("The server is ready to receive")
        # ACA TENDRIAMOS QUE HACER UN LISTENER Y ACCEPTER Y LANZAR UN HILO POR CADA CLIENTE?
        while True:
            # Se recibe directamente, no hay pasos previos
            # como "accept" o "listen" para el handshaking
            message, clientAddress = serverSocket.recvfrom(2048)
            # Tomo Client Address, vean que Port imprime:
            print("Client Address: ", clientAddress)
            modifiedMessage = message.decode().upper()
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            print("Message sent")
            if modifiedMessage == "FIN":
                break
        serverSocket.close()
        return
