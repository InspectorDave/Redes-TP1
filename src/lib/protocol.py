import socket
from lib.constants import BUFFER_SIZE, PAYLOAD_SIZE, FILE_MODE_READ, FILE_MODE_WRITE
from lib.message import *
from lib.file_manager import *

class Protocol:

    UPLOAD = 0
    DOWNLOAD = 1
    STOP_AND_WAIT = 0
    GO_BACK_N = 1

    def __init__(self):
        return

    # - Capaz que es mejor pasarle el file manager por parametro
    # y que se maneje desde afuera. El send solo debería
    # ocuparse de enviar la info que le pasan
    # - El send solo se ocupa de codificar la info en un paquete
    def send(self, file_path, client_socket, host, port):
        offset = 0
        ack_number = 0
        packet_number = 0
        message_type = Message.SEND
        transfer_type = Protocol.UPLOAD
        protocol_type = Protocol.STOP_AND_WAIT
        file_manager = FileManager(FILE_MODE_READ, file_path)
        file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        while file_chunk:
            message = Message(message_type, transfer_type,protocol_type, packet_number, ack_number, offset, file_chunk)
            message_bytes = message.encode()
            sent = client_socket.sendto(message_bytes, (host, port))
            offset += len(file_chunk)
            packet_number += 1
            ack_number += 1
            print(f"[LOG] {sent} bytes sent")
            file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        file_manager.close()
        return

    # El receive solo se ocupa de recibir un paquete y decodificarlo
    def receive(self, client_socket):
        message_received, serverAddress = client_socket.recvfrom(BUFFER_SIZE)
        msg_decoded = Message.decode(message_received)
        return msg_decoded
    
    # Desde fuera de esta clase se debería abrir el doc, ir recibiendo y
    # escribiendo y cerrar al final
    #def process_message(self, message):
    #    return
    
    def send_ack():
        return
    
    def receive_ack():
        return