from socket import *
from threading import *
from lib.constants import *

from lib.message import *

from lib.protocols.protocol import Protocol
from lib.protocols.stop_and_wait import StopAndWaitProtocol
from lib.protocols.go_back_n import GoBackNProtocol
from lib.protocols.protocol_factory import ProtocolFactory
import logging
from lib.logging_msg import *

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
        logging.info(f"{MSG_SERVER_READY_TO_RECEIVE}")

        while True:

            message, clientAddress = Protocol.decode_received_message(serverSocket)
            self.__process_new_connetion(message, clientAddress)

    def __process_new_connetion(self, message, clientAddress):
        logging.info(f"{MSG_PROCESSING_NEW_CONNECTION}")

        if message.message_type != Message.INITIATE:
            logging.debug(f"{MSG_IS_NOT_INITIATE}")
            return
        if clientAddress in self.clients:
            # El cliente ya estaba conectado
            logging.debug(f"{MSG_CLIENT_ALREADY_HAS_ASSIGNED_CONNECTION}")
            return

        logging.debug(f"{MSG_RECEIVED_INITIATE}")

        new_thread = Thread(target=self.__process_existing_connection, args=(clientAddress, message))
        new_thread.start()
        self.clients.append(clientAddress)

        logging.info(f"{MSG_PROCESSED_NEW_CONNECTION}")

        return
    
    def __process_existing_connection(self, clientAddress, message_initiate):

        logging.debug(f"{MSG_PROCESSING_EXISTING_CONNECTION}")

        session_protocol = ProtocolFactory.create(message_initiate.protocol_type)

        dedicatedClientSocket = socket(AF_INET, SOCK_DGRAM)
        dedicatedClientSocket.bind((self.host,0))

        sendInack(dedicatedClientSocket, clientAddress, message_initiate.transfer_type, message_initiate.protocol_type)

        message, clientAddress = Protocol.decode_received_message(dedicatedClientSocket)

        if message.message_type != Message.ESTABLISHED:
            logging.debug(f"{MSG_IS_NOT_ESTABLISHED}")
            return
        
        logging.debug(f"{MSG_IS_ESTABLISHED} {message.filename}")

        thread_manager = Condition()
        communication_queue = []

        thread_receiver = Thread(target=session_protocol.downloader_receiver_logic, args=(dedicatedClientSocket, thread_manager, communication_queue, self.storage, message.filename,))
        thread_receiver.start()
    
        thread_sender = Thread(target=session_protocol.downloader_sender_logic, args=(dedicatedClientSocket, clientAddress[0], clientAddress[1], thread_manager, communication_queue,))
        thread_sender.start()
        return

def sendInack (dedicatedClientSocket, clientAddress, transfer_type, protocol_type):

    logging.debug(f"{MSG_SENDING_INACK}")

    message = Inack(transfer_type, protocol_type)
    message_encoded = message.encode()

    dedicatedClientSocket.sendto(message_encoded, clientAddress)

    logging.debug(f"{MSG_SENT_INACK}")

    return
