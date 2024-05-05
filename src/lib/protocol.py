import socket
from lib.constants import BUFFER_SIZE, PAYLOAD_SIZE
from lib.message import *
from lib.file_manager import *

class Protocol:

    UPLOAD = 0
    DOWNLOAD = 1

    def __init__(self):
        return

    def send(self, file_path, client_socket, host, port):
        offset = 0
        ack_number = 0
        packet_number = 0
        message_type = Message.SEND
        transfer_type = Protocol.UPLOAD
        file_manager = FileManager(file_path)
        file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        while file_chunk:
            message = Message(message_type, transfer_type, packet_number, ack_number, offset, file_chunk)
            message_bytes = message.encode()
            sent = client_socket.sendto(message_bytes, (host, port))
            offset += len(file_chunk)
            packet_number += 1
            ack_number += 1
            print(f"[LOG] {sent} bytes sent")
            file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        file_manager.close()
        return


    def receive(self, client_socket):
        modifiedMessage, serverAddress = client_socket.recvfrom(BUFFER_SIZE)
        return modifiedMessage