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
        self.connection.destination_host, self.connection.destination_port = server_address
        return

    def upload(self):
        thread_receiver = Thread(target = self.connection.protocol.uploader_receiver_logic,\
                                 args = (self.connection,))
        thread_receiver.start()
        thread_sender = Thread(target = self.connection.protocol.uploader_sender_logic,\
                               args = (self.connection, self.file_path))
        thread_sender.start()

        return
    
    def download(self):
        thread_receiver = Thread(target = self.connection.protocol.downloader_receiver_logic,\
                                 args = (self.connection, self.file_path))
        thread_receiver.start()
        thread_sender = Thread(target = self.connection.protocol.downloader_sender_logic,\
                               args = (self.connection,))
        thread_sender.start()

        return
