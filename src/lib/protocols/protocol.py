import socket
from lib.constants import *
from lib.message import *
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
    
    def perform_client_side_handshake(self, client):
        logging.info(f"{MSG_HANDSHAKE_STARTING}")
        client.reset_timer()

        while True:
            message = Initiate(client.transfer_type, client.protocol.CODE)
            self.send_initiate(client.socket, client.server_host, client.server_port, message)

            try:
                decoded_message, downloader_address = self.decode_received_message(client.socket)
            except TimeoutError:
                if client.end_process.is_set():
                    exit()
                continue
            client.reset_timer()
            if verify_inack(decoded_message, client.transfer_type, client.protocol.CODE):
                break

        self.send_established(client.socket, downloader_address[0], downloader_address[1], client.file_name)

        logging.info(f"{MSG_HANDSHAKE_COMPLETED}")
        client.keep_alive_timer.cancel()
        return downloader_address

    def send_initiate(self, socket, host, port, message):
        logging.info(f"[LOG] Sending INITIATE")
        self.send_message(socket, host, port, message)
        return
    
    def receive_inack(self, socket, host, port):
        message_decoded, server_address = self.receive(socket)

        if message_decoded.message_type != Message.INACK:
            logging.debug(f"{MSG_IS_NOT_INACK}")
            return

        logging.debug(f"{MSG_RECEIVED_INACK}")

        return server_address

    def send_established(self, socket, host, port, filename):
        logging.info(f"{MSG_SENDING_ESTABLISHED}")
        logging.debug(f"{MSG_FILE_NAME} {filename}")
        message = Established(filename)
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

def verify_inack(message, transfer_type, protocol):
    if message.message_type != Message.INACK:
        logging.debug(f"{MSG_IS_NOT_INACK}")
        return False
    if message.transfer_type != transfer_type:
        logging.debug(f"{MSG_TRANSFER_TYPE_NOT_MATCH}")
        return False
    if message.protocol_type != protocol:
        logging.debug(f"{MSG_PROTOCOL_NOT_MATCH}")
        return False
    logging.debug(f"{MSG_RECEIVED_INACK}")
    return True