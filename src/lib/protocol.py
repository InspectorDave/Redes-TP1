import socket
from lib.constants import BUFFER_SIZE, PAYLOAD_SIZE
from lib.message import *

class Protocol:

    UPLOAD = 0
    DOWNLOAD = 1

    def __init__(self):
        return

    def send(self, file_content, client_socket, host, port):
        total_length = len(file_content)
        message_type = Message.SEND
        transfer_type = Protocol.UPLOAD
        offset = 0
        ack_number = 0
        packet_number = 0
        while offset < total_length:
            # Obtener el siguiente bloque de datos
            block = file_content[offset:offset + PAYLOAD_SIZE]
            message = Message(message_type, transfer_type, packet_number, ack_number, offset, block)
            message_bytes = message.encode()
            
            # Enviar el bloque de datos al servidor
            sent = client_socket.sendto(message_bytes, (host, port))
            
            offset += len(block)
            packet_number += 1
            ack_number += 1
            
            # Aquí puedes realizar cualquier otra operación relacionada con el envío
            print(f"[LOG] {sent} bytes sent")
        #client_socket.sendto(file_content,(host, port))
        return
    
    def receive(self, client_socket):
        modifiedMessage, serverAddress = client_socket.recvfrom(BUFFER_SIZE)
        return modifiedMessage