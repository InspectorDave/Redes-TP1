from socket import *
from threading import Thread
from threading import Lock
from lib.constants import *
from lib.message import *

class Server:
    def __init__(self, host, port, args):
        self.host = host
        self.port = port
        self.clients = {}
        if (args.storage is None):
            self.storage = DEFAULT_SERVER_STORAGE
        else:
            self.storage = args.storage
    
    def start(self):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind((self.host, self.port))
        print("The server is ready to receive")
        # ACA TENDRIAMOS QUE HACER UN LISTENER Y ACCEPTER Y LANZAR UN HILO POR CADA CLIENTE?
        while True:
            # Se recibe directamente, no hay pasos previos
            # como "accept" o "listen" para el handshaking
            message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
            # Tomo Client Address, vean que Port imprime:
            print("Client Address: ", clientAddress)
            print("Bytes recibidos: ", len(message))
            msg_decoded = Message(0,0,0,0)
            message_decoded = msg_decoded.decode(message)
            if len(message_decoded.payload) < PAYLOAD_SIZE:
                break
        serverSocket.close()
        return
