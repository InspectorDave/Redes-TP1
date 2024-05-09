import logging
from socket import *
from threading import *

from lib.message import *
from lib.logging_msg import *
from lib.constants import *
from lib.connection import Connection

class Client:
    def __init__(self, connection, file_path):
        self.connection = connection
        self.file_path = file_path
        return

    def start(self):
        self.connection.socket.settimeout(TIME_OUT)
        server_address = self.connection.protocol.perform_client_side_handshake(self.connection)
        self.connection.server_host, self.connection.server_port = server_address
        return

    def upload(self):
        
        communication_queue = []

        thread_receiver = Thread(target=self.connection.protocol.uploader_receiver_logic,\
                                 args=(self.connection, communication_queue))
        thread_receiver.start()
        thread_sender = Thread(target=self.connection.protocol.uploader_sender_logic,\
                               args=(self.connection, self.file_path, communication_queue))
        thread_sender.start()
        return
    
    def download(self, file_path, filename):
        logging.info(f"{MSG_PROCESSING_NEW_CONNECTION}")

        connection = Connection((self.destination_host, self.destination_port), self.transfer_type, self.protocol, filename)
        connection.keep_alive_timer.start()
        communication_queue = []

        connection.socket.settimeout(TIME_OUT)

        thread_receiver = Thread(target=connection.protocol.downloader_receiver_logic, args=(connection, communication_queue, file_path))
        thread_receiver.start()
        thread_sender = Thread(target=connection.protocol.downloader_sender_logic, args=(connection, communication_queue))
        thread_sender.start()

        return
