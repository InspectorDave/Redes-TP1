from socket import AF_INET, SOCK_DGRAM, socket
from threading import Thread
import logging

import lib.constants as CONST
from lib.protocols.protocol import Protocol
import lib.logging_msg as MSG


class Server:
    def __init__(self, host, port, args):
        self.host = host
        self.port = port
        self.clients = []
        self.storage = args.storage

    def start(self):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind((self.host, self.port))
        logging.info(f"{MSG.MSG_SERVER_READY_TO_RECEIVE}")

        while True:
            message, clientAddress = Protocol.decode_received_message(serverSocket)
            new_connection_thread = Thread(target=self.__process_new_connetion, args=(message, clientAddress))
            new_connection_thread.start()

    def __process_new_connetion(self, message, clientAddress):
        logging.info(f"{MSG.MSG_PROCESSING_NEW_CONNECTION}")

        connection = Protocol.perform_server_side_handshake(self, message, clientAddress)
        connection.timeout_timer.start()

        connection.socket.settimeout(CONST.TIME_OUT)

        thread_receiver = None
        thread_sender = None

        match connection.transfer_type:
            case Protocol.UPLOAD:
                # The server is the downloader
                logging.info(f"{MSG.MSG_DOWNLOADING_FILE} {MSG.MSG_WITH_PROTOCOL} {connection.protocol.__class__.__name__}")
                thread_receiver = Thread(target=connection.protocol.downloader_receiver_logic,
                                         args=(connection, self.storage))
                thread_sender = Thread(target=connection.protocol.downloader_sender_logic,
                                       args=(connection,))
            case Protocol.DOWNLOAD:
                # The server is the uploader
                logging.info(f"{MSG.MSG_UPLOADING_FILE} {MSG.MSG_WITH_PROTOCOL} {connection.protocol.__class__.__name__}")
                thread_receiver = Thread(target=connection.protocol.uploader_receiver_logic,
                                         args=(connection,))
                thread_sender = Thread(target=connection.protocol.uploader_sender_logic,
                                       args=(connection, self.storage))

        thread_receiver.start()
        thread_sender.start()
        thread_sender.join()
        thread_receiver.join()
        self.clients.remove(clientAddress)
        logging.info(f"{MSG.MSG_CONNECTION_ENDED}")
        return
