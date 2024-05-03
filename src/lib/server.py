from socket import *
from threading import Thread
from threading import Lock
from lib.constants import *
from lib.message import *

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
            # Cada mensaje se procesa en un thread a parte. De esta manera no se rompe
            # si llegan dos mensajes al mismo tiempo.

            message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)

            self.__process_new_connetion(message, clientAddress)

    def __process_new_connetion(self, message, clientAddress):
        print("Processing new connection...")
        
        print(Message.decode(message).message_type)

        return

        if message_decoded.packet_number != 16:
            # El mensaje no es una nueva conexión
            print("El mensaje no es una nueva conexión")
            return
        if clientAddress in self.clients:
            # El cliente ya está conectado
            print("El mensaje no es una nueva conexión")
            return

        # Creo un nuevo thread para el nuevo cliente
        new_thread = Thread(target=self.__process_existing_connection, args=(clientAddress))
        new_thread.run()      
        self.clients.append(clientAddress)

        print("Processed new connection.")

        return
    
    def __process_existing_connection(self, clientAddress):

        print("Processing existing connection.")

        dedicatedClientSocket = socket(AF_INET, SOCK_DGRAM)
        dedicatedClientSocket.bind((self.host, self.port))

        sendInack(dedicatedClientSocket, clientAddress)

        message, clientAddress = dedicatedClientSocket.recvfrom(BUFFER_SIZE)
        # Tomo Client Address, vean que Port imprime:
        print("Client Address: ", clientAddress)
        print("Bytes recibidos: ", len(message))
        msg_decoded = Message(0,0,0,0)
        # message_decoded = msg_decoded.decode(message)

        print("Processed new connection.")

        return
    
def sendInack (dedicatedClientSocket, clientAddress):

    print("Sending inack...")

    message = Message(17, 0, 0, 0)

    dedicatedClientSocket.sendto(message, clientAddress)

    print("Sent inack.")

    return