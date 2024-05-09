from socket import *
from threading import *
import logging

from lib.constants import *
from lib.message import *
from lib.protocols.protocol import Protocol
from lib.logging_msg import *

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
        connection.keep_alive_timer.start()

        connection.socket.settimeout(TIME_OUT)

        match connection.transfer_type:
            case Protocol.UPLOAD:
            # The server is the downloader
                logging.info(f"{MSG_DOWNLOADING_FILE}")
                thread_receiver = Thread(target=connection.protocol.downloader_receiver_logic,\
                                         args=(connection, self.storage))
                thread_receiver.start()
                thread_sender = Thread(target=connection.protocol.downloader_sender_logic,\
                                       args=(connection,))
                thread_sender.start()
                return
            case Protocol.DOWNLOAD:
            # The server is the uploader
                logging.info(f"{MSG_UPLOADING_FILE}")
                thread_receiver = Thread(target=connection.protocol.uploader_receiver_logic,\
                                         args=(connection,))
                thread_receiver.start()
                thread_sender = Thread(target=connection.protocol.uploader_sender_logic,\
                                       args=(connection, self.storage))
                thread_sender.start()
        return
