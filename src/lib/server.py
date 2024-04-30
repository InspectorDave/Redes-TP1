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

        while True:
            # Cada mensaje se procesa en un thread a parte. De esta manera no se rompe
            # si llegan dos mensajes al mismo tiempo.
            new_thread = Thread(target=self.__process_message, args=(serverSocket,))
            new_thread.run()

    def __process_message(self, serverSocket):
        message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
        # Tomo Client Address, vean que Port imprime:
        print("Client Address: ", clientAddress)
        print("Bytes recibidos: ", len(message))
        msg_decoded = Message(0,0,0,0)
        # message_decoded = msg_decoded.decode(message)

        return
