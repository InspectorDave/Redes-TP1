from socket import *
from threading import *
import logging

from lib.constants import *
from lib.message import *
from lib.protocols.protocol import Protocol

from lib.logging_msg import *
from lib.client import Connection

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
            new_connection_thread = Thread(target=self.__process_new_connetion, args=(message, clientAddress))
            new_connection_thread.start()

    def __process_new_connetion(self, message, clientAddress):
        logging.info(f"{MSG_PROCESSING_NEW_CONNECTION}")

        connection = Protocol.perform_server_side_handshake(self, message, clientAddress)

        communication_queue = []

        thread_receiver = Thread(target=connection.protocol.downloader_receiver_logic, args=(connection.socket, connection.thread_manager, communication_queue, self.storage, connection.file_name))
        thread_receiver.start()
    
        thread_sender = Thread(target=connection.protocol.downloader_sender_logic, args=(connection.socket, connection.destination_host, connection.destination_port, connection.thread_manager, communication_queue))
        thread_sender.start()

        return
