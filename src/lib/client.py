from socket import *
from lib.message import *
from lib.logging_msg import *
from lib.constants import *
from threading import *
import logging

class Connection:
    def __init__(self, destination_address, transfer_type, protocol, file_name):
        self.destination_host = destination_address[0]
        self.destination_port = destination_address[1]
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.file_name = file_name
        self.protocol = protocol
        self.transfer_type = transfer_type
        self.keep_alive_timer = Timer(KEEP_ALIVE, self.end_connection)
        self.end_connection_flag = Event()
        self.thread_manager = Condition()

    def close_socket():
        socket.shutdown(SHUT_RDWR)
        socket.close()
        return
    
    def reset_timer(self):
        self.keep_alive_timer.cancel()
        self.keep_alive_timer = Timer(KEEP_ALIVE, self.end_connection)
        self.keep_alive_timer.start()
        return

    def end_connection(self):
        logging.info(f"{MSG_KEEP_ALIVE_TIMEOUT}")
        self.keep_alive_timer.cancel()
        self.end_connection_flag.set()
        return

class Client(Connection):
    def start(self):
        self.socket.settimeout(TIME_OUT)
        server_address = self.protocol.perform_client_side_handshake(self)
        self.server_host, self.server_port = server_address
        return

    def upload(self, file_path, filename):
        
        communication_queue = []

        thread_receiver = Thread(target=self.protocol.uploader_receiver_logic, args=(self, communication_queue))
        thread_receiver.start()
    
        thread_sender = Thread(target=self.protocol.uploader_sender_logic, args=(self, file_path, filename, communication_queue))
        thread_sender.start()
        return
    
    def download(self):
        complete_file = self.protocol.receive_file(socket)
        return complete_file
