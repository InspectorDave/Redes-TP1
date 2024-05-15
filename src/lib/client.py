import logging
from threading import Thread

import lib.logging_msg as MSG
import lib.constants as CONST


class Client:
    def __init__(self, connection, file_path):
        self.connection = connection
        self.file_path = file_path
        return

    def start(self):
        self.connection.socket.settimeout(CONST.TIME_OUT)
        server_address = self.connection.protocol.perform_client_side_handshake(self.connection)
        self.connection.destination_host, self.connection.destination_port = server_address
        return

    def upload(self):
        thread_receiver = Thread(target=self.connection.protocol.uploader_receiver_logic,
                                 args=(self.connection,))
        thread_sender = Thread(target=self.connection.protocol.uploader_sender_logic,
                               args=(self.connection, self.file_path))

        self.run_threads(thread_receiver, thread_sender)
        return

    def download(self):
        thread_receiver = Thread(target=self.connection.protocol.downloader_receiver_logic,
                                 args=(self.connection, self.file_path))

        thread_sender = Thread(target=self.connection.protocol.downloader_sender_logic,
                               args=(self.connection,))

        self.run_threads(thread_receiver, thread_sender)
        return

    def run_threads(self, thread_receiver, thread_sender):
        thread_receiver.start()
        thread_sender.start()
        thread_sender.join()
        thread_receiver.join()
        logging.info(f"{MSG.MSG_CONNECTION_ENDED}")
        return
