import socket
from lib.constants import *
from lib.messages.message import *
from lib.messages.initiate import Initiate
from lib.messages.inack import Inack
from lib.file_manager import *
import logging
from lib.logging_msg import *

TIME_OUT = 2

class Protocol:

    UPLOAD = 0
    DOWNLOAD = 1
    STOP_AND_WAIT = 0
    GO_BACK_N = 1

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
        logging.error(f"{MSG_SEND_FILE_METHOD_NOT_IMPLEMENTED}")
        raise NotImplementedError(f"{MSG_SEND_FILE_METHOD_NOT_IMPLEMENTED}")
    
    # Se encarga de recibir el archivo e ir escribiendolo
    def receive_file(self,client_socket:socket.socket):
        logging.error(f"{MSG_RECEIVE_FILE_METHOD_NOT_IMPLEMENTED}")
        raise NotImplementedError(f"{MSG_RECEIVE_FILE_METHOD_NOT_IMPLEMENTED}")

    # El receive solo se ocupa de recibir un paquete y decodificarlo
    def receive(self, client_socket:socket.socket):

        message, serverAddress = Protocol.decode_received_message(client_socket)
        return message, serverAddress
    
    def send_ack(self):
        return
    
    def receive_ack(self):
        return
    
    def perform_client_side_handshake(self, socket, host, port):
        logging.info(f"{MSG_HANDSHAKE_STARTING}")
        self.send_initiate(socket, host, port)
        comm_server_address = self.receive_inack(socket, host, port)
        self.send_established(socket, comm_server_address[0], comm_server_address[1])
        logging.info(f"{MSG_HANDSHAKE_COMPLETED}")
        return comm_server_address

    def send_initiate(self, socket, host, port):
        logging.info(f"[LOG] Sending INITIATE")
        message = Initiate(Protocol.UPLOAD, Protocol.STOP_AND_WAIT)
        self.send_message(socket, host, port, message)
        return
    
    def receive_inack(self, socket, host, port):
        message_decoded, server_address = self.receive(socket)

        if message_decoded.message_type != Message.INACK:
            logging.debug(f"{MSG_IS_NOT_INACK}")
            return

        logging.debug(f"{MSG_RECEIVED_INACK}")

        return server_address

    def send_established(self, socket, host, port):
        logging.info(f"{MSG_SENDING_ESTABLISHED}")
        message = Established()
        self.send_message(socket, host, port, message)
        return

    @staticmethod
    def decode_received_message(socket:socket.socket):
        recv_buffer, clientAddress = socket.recvfrom(RECV_BUFFER_SIZE)
        fixed_header = recv_buffer[:Message.FIXED_HEADER_SIZE]
        recv_buffer = recv_buffer[Message.FIXED_HEADER_SIZE:]
        message_type = Decoder.decode_fixed_header(fixed_header)
        rest_of_message = recv_buffer
        decoded_message = Decoder.decode_after_fixed_header(message_type, rest_of_message)

        logging.debug(f"{MSG_RECEIVED_MSG_TYPE} {decoded_message.message_type}")
        logging.debug(f"{MSG_BYTES_RECEIVED} {len(rest_of_message) + len(fixed_header)}")

        return decoded_message, clientAddress
