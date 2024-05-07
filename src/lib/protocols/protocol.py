import socket
from lib.constants import *
from lib.message import *
from lib.file_manager import *
import logging

TIME_OUT = 3

class Protocol:

    UPLOAD = 0
    DOWNLOAD = 1
    STOP_AND_WAIT = 0
    GO_BACK_N = 1

    def __init__(self):
        self.packet_number = 0
        self.ack_number = 0
        self.offset = 0
        return

    # Recibe un socket, host, port y mensaje a enviar,
    # lo codifica y lo envia
    def send_message(self, client_socket:socket.socket, host, port, message:Message):
        message_bytes = message.encode()
        sent = client_socket.sendto(message_bytes, (host, port))
        return sent

    # Recibe un archivo, socket, host, port
    # Se encarga de leer el archivo, setear los nros
    # de paquetes, acks, etc y lo envia
    def send_file(self, file_path, client_socket, host, port):
        logging.error(f"El metodo 'send_file' debe ser implementado por la subclase")
    
    # Se encarga de recibir el archivo e ir escribiendolo
    def receive_file(self,client_socket:socket.socket):
        logging.error(f"El metodo 'receive_file' debe ser implementado por la subclase")

    # El receive solo se ocupa de recibir un paquete y decodificarlo
    def receive(self, client_socket:socket.socket):
        message_received, serverAddress = client_socket.recvfrom(BUFFER_SIZE)
        msg_decoded = Message.decode(message_received)
        return msg_decoded, serverAddress
    
    def send_ack(self):
        return
    
    def receive_ack(self):
        return
    
    def perform_client_side_handshake(self, socket, host, port):
        logging.info(f"[LOG] Handshake starting...")
        self.send_initiate(socket, host, port)
        comm_server_address = self.receive_inack(socket, host, port)
        self.send_senack(socket, comm_server_address[0], comm_server_address[1])
        logging.info(f"[LOG] Handshake completed")
        return comm_server_address

    def send_initiate(self, socket, host, port):
        logging.info(f"[LOG] Sending INITIATE")
        message = Message(Message.INITIATE, Protocol.UPLOAD, Protocol.STOP_AND_WAIT, 0, 0, 0, b'')
        self.send_message(socket, host, port, message)
        return
    
    def receive_inack(self, socket, host, port):
        message_decoded, server_address = self.receive(socket)

        if message_decoded.message_type != Message.INACK:
            print(f"[LOG] Message isn't Inack")
            return

        print(f"[LOG] Received an Inack")

        return server_address

    def send_senack(self, socket, host, port):
        print(f"[LOG] Sending SENACK")
        message = Message(Message.SENACK, Protocol.UPLOAD,Protocol.STOP_AND_WAIT, 0, 0, 0, b'')
        self.send_message(socket, host, port, message)
        return
