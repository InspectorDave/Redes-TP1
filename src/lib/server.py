from socket import *
from threading import Thread
from threading import Lock
from lib.constants import *
from lib.message import *
from lib.protocol import Protocol

import time

class Server:
    def __init__(self, host, port, args):
        self.host = host
        self.port = port
        self.clients = []
        if (args.storage is None):
            self.storage = DEFAULT_SERVER_STORAGE
        else:
            self.storage = args.storage
    
    def start(self):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind((self.host, self.port))
        print("The server is ready to receive")

        while True:
            message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
            self.__process_new_connetion(message, clientAddress)

    def __process_new_connetion(self, message, clientAddress):
        print("[LOG] Processing new connection...")
        
        message_decoded = Initiate.decode(message)

        if message_decoded.message_type != Message.INITIATE:
            # El mensaje no es una nueva conexión
            print("[LOG] Message isn't INITIATE")
            return
        if clientAddress in self.clients:
            # El cliente ya está conectado
            print("[LOG] Client already has an assigned connection")
            return

        print("[LOG] Received INITIATE")

        # Creo un nuevo thread para el nuevo cliente
        new_thread = Thread(target=self.__process_existing_connection, args=(clientAddress,))
        new_thread.run()
        self.clients.append(clientAddress)

        print("[LOG] Processed new connection.")

        return
    
    def __process_existing_connection(self, clientAddress):

        print("[LOG] Processing an existing connection...")

        dedicatedClientSocket = socket(AF_INET, SOCK_DGRAM)
        dedicatedClientSocket.bind((self.host,0))

        sendInack(dedicatedClientSocket, clientAddress)

        # message, clientAddress = dedicatedClientSocket.recvfrom(BUFFER_SIZE)
        # # Tomo Client Address, vean que Port imprime:
        # print("Client Address: ", clientAddress)
        # print("Bytes recibidos: ", len(message))
        # msg_decoded = Message(0,0,0,0)
        # # message_decoded = msg_decoded.decode(message)

        print("[LOG] Processed existing connection.")

        return
    
def sendInack (dedicatedClientSocket, clientAddress):

    print("[LOG] Sending inack...")

    message = Inack(Protocol.UPLOAD)
    message_encoded = message.encode()

    dedicatedClientSocket.sendto(message_encoded, clientAddress)

    print("[LOG] Sent inack.")

    return