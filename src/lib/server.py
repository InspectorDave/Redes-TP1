from socket import *
from threading import *
from lib.constants import *
from lib.message import *
from lib.protocols.protocol import Protocol
from lib.protocols.stop_and_wait import StopAndWaitProtocol
from lib.protocols.go_back_n import GoBackNProtocol
from lib.protocols.protocol_factory import ProtocolFactory
import logging

import time

class Server:
    def __init__(self, host, port, args):
        self.host = host
        self.port = port
        self.clients = []
        self.storage = args.storage
    
    def start(self):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind((self.host, self.port))
        print(f"The server is ready to receive")

        while True:
            message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
            self.__process_new_connetion(message, clientAddress)

    def __process_new_connetion(self, message, clientAddress):
        logging.info(f"[LOG] Processing new connection...")
        
        message_decoded = Message.decode(message)

        if message_decoded.message_type != Message.INITIATE:
            # El mensaje no es una nueva conexión
            logging.debug(f"[LOG] Message isn't INITIATE")
            return
        if clientAddress in self.clients:
            # El cliente ya estaba conectado
            logging.debug(f"[LOG] Client already has an assigned connection")
            return

        logging.debug(f"[LOG] Received INITIATE")

        # Creo un nuevo thread para el nuevo cliente
        new_thread = Thread(target=self.__process_existing_connection, args=(clientAddress,))
        new_thread.start()
        self.clients.append(clientAddress)

        logging.info(f"[LOG] Processed new connection.")

        return
    
    def __process_existing_connection(self, clientAddress):

        print(f"[LOG] Processing an existing connection...")

        dedicatedClientSocket = socket(AF_INET, SOCK_DGRAM)
        dedicatedClientSocket.bind((self.host,0))

        sendInack(dedicatedClientSocket, clientAddress)

        message, clientAddress = dedicatedClientSocket.recvfrom(BUFFER_SIZE)

        decoded_message = Message.decode(message)
        logging.debug(f"[LOG] Received message type: {decoded_message.message_type}")

        if decoded_message.message_type != Message.SENACK:
            print(f"[LOG] Message isn't SENACK")
            return

        session_protocol = ProtocolFactory.create(decoded_message.protocol_type)

        thread_manager = Condition()
        communication_queue = []

        thread_receiver = Thread(target=session_protocol.downloader_receiver_logic, args=(dedicatedClientSocket, thread_manager, communication_queue, self.storage,))
        thread_receiver.start()
    
        thread_sender = Thread(target=session_protocol.downloader_sender_logic, args=(dedicatedClientSocket, clientAddress[0], clientAddress[1], thread_manager, communication_queue,))
        thread_sender.start()
        return

def sendInack (dedicatedClientSocket, clientAddress):

    print(f"[LOG] Sending inack...")

    message = Message(Message.INACK, Protocol.UPLOAD,Protocol.STOP_AND_WAIT, 0, 0, b'')
    message_encoded = message.encode()

    dedicatedClientSocket.sendto(message_encoded, clientAddress)

    print(f"[LOG] Sent inack.")

    return
