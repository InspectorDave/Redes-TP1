from socket import *
from threading import *
import logging

from lib.constants import *
from lib.logging_msg import *


class Connection:
    def __init__(self, destination_address, transfer_type, protocol, file_name):
        self.destination_host = destination_address[0]
        self.destination_port = destination_address[1]
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.file_name = file_name
        self.transfer_type = transfer_type
        self.protocol = protocol
        self.thread_manager = Condition()
        self.sender_receiver_communication_queue = []
        self.end_connection_flag = Event()
        self.timeout_time = IDLE_TIMEOUT
        self.timeout_timer = Timer(self.timeout_time, self.end_connection)

    def wake_up_threads(self):
        self.thread_manager.acquire()
        self.thread_manager.notify()
        self.thread_manager.release()
        return

    def reset_timer(self):
        self.timeout_timer.cancel()
        self.timeout_timer = Timer(self.timeout_time, self.end_connection)
        self.timeout_timer.start()
        return

    def end_connection(self):
        logging.info(f"{MSG_KEEP_ALIVE_TIMEOUT}")
        self.timeout_timer.cancel()
        self.end_connection_flag.set()
        self.wake_up_threads()
        return
