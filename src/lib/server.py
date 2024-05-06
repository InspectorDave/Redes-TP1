from socket import *
from threading import *
from lib.constants import *
from lib.message import *
from lib.protocols.protocol import Protocol
from lib.protocols.stop_and_wait import StopAndWaitProtocol
from lib.protocols.go_back_n import GoBackNProtocol
from lib.protocols.protocol_factory import ProtocolFactory

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
        
        message_decoded = Message.decode(message)

        if message_decoded.message_type != Message.INITIATE:
            # El mensaje no es una nueva conexión
            print("[LOG] Message isn't INITIATE")
            return
        if clientAddress in self.clients:
            # El cliente ya estaba conectado
            print("[LOG] Client already has an assigned connection")
            return

        print("[LOG] Received INITIATE")

        # Creo un nuevo thread para el nuevo cliente
        new_thread = Thread(target=self.__process_existing_connection, args=(clientAddress,))
        new_thread.start()
        self.clients.append(clientAddress)

        print("[LOG] Processed new connection.")

        return
    
    def __process_existing_connection(self, clientAddress):

        print("[LOG] Processing an existing connection...")

        dedicatedClientSocket = socket(AF_INET, SOCK_DGRAM)
        dedicatedClientSocket.bind((self.host,0))

        sendInack(dedicatedClientSocket, clientAddress)

        message, clientAddress = dedicatedClientSocket.recvfrom(BUFFER_SIZE)

        decoded_message = Message.decode(message)
        print("[LOG] Received message type: ", decoded_message.message_type)

        if decoded_message.message_type != Message.SENACK:
            print("[LOG] Message isn't SENACK")
            return

        session_protocol = ProtocolFactory.create(decoded_message.protocol_type)

        thread_manager = Condition()
        communication_queue = []

        thread_receiver = Thread(target=session_protocol.downloader_receiver_logic, args=(dedicatedClientSocket, thread_manager, communication_queue,))
        thread_receiver.start()
    
        thread_sender = Thread(target=session_protocol.downloader_sender_logic, args=(dedicatedClientSocket, thread_manager, communication_queue,))
        thread_sender.start()
        return

def sendInack (dedicatedClientSocket, clientAddress):

    print("[LOG] Sending inack...")

    message = Message(Message.INACK, Protocol.UPLOAD,Protocol.STOP_AND_WAIT, 0, 0, 0, b'')
    message_encoded = message.encode()

    dedicatedClientSocket.sendto(message_encoded, clientAddress)

    print("[LOG] Sent inack.")

    return
