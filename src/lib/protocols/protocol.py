from socket import *
from threading import *
from lib.constants import *
from lib.message import *
from lib.file_manager import *
import logging
from lib.logging_msg import *
from lib.client import Connection


class Protocol:

    UPLOAD = 0
    DOWNLOAD = 1
    STOP_AND_WAIT = 0
    GO_BACK_N = 1

    # Recibe un socket, host, port y mensaje a enviar,
    # lo codifica y lo envia
    @staticmethod
    def send_message(client_socket: socket, host, port, message: Message):
        message_bytes = message.encode()
        sent = client_socket.sendto(message_bytes, (host, port))
        return sent

    # El receive solo se ocupa de recibir un paquete y decodificarlo
    @staticmethod
    def receive(client_socket: socket):
        message, serverAddress = Protocol.decode_received_message(client_socket)
        return message, serverAddress

    @staticmethod
    def perform_client_side_handshake(connection):
        logging.info(f"{MSG_HANDSHAKE_STARTING}")
        connection.reset_timer()

        while True:
            message = Initiate(connection.transfer_type, connection.protocol.CODE)
            Protocol.send_initiate(connection.socket, connection.destination_host, connection.destination_port, message)

            try:
                decoded_message, downloader_address = Protocol.decode_received_message(connection.socket)
            except TimeoutError:
                if connection.end_connection_flag.is_set():
                    exit()
                continue
            connection.reset_timer()
            if Protocol.verify_inack(decoded_message, connection.transfer_type, connection.protocol.CODE):
                break

        Protocol.send_established(connection.socket, downloader_address[0], downloader_address[1], connection.file_name)

        logging.info(f"{MSG_HANDSHAKE_COMPLETED}")
        return downloader_address

    @staticmethod
    def perform_server_side_handshake(server, first_message, client_address):
        logging.info(f"{MSG_HANDSHAKE_STARTING}")

        Protocol.process_initiate(first_message, client_address, server)

        from lib.protocols.protocol_factory import ProtocolFactory
        session_protocol = ProtocolFactory.create(first_message.protocol_type)

        dedicated_client_socket = socket(AF_INET, SOCK_DGRAM)
        dedicated_client_socket.bind((server.host, 0))
        Protocol.sendInack(dedicated_client_socket, client_address, first_message)

        dedicated_client_socket.settimeout(IDLE_TIMEOUT)
        try:
            established_message, client_address = Protocol.decode_received_message(dedicated_client_socket)
        except TimeoutError:
            logging.info(f"{MSG_KEEP_ALIVE_TIMEOUT}")
            logging.warn(f"{MSG_ESTABLISHED_NOT_RECEIVED}")
            exit()

        if established_message.message_type != Message.ESTABLISHED:
            logging.debug(f"{MSG_IS_NOT_ESTABLISHED}")
            exit()
        logging.debug(f"{MSG_IS_ESTABLISHED} {established_message.filename}")

        connection = Connection(client_address, first_message.transfer_type, session_protocol, established_message.filename)
        dedicated_client_socket.settimeout(None)
        connection.socket = dedicated_client_socket

        logging.info(f"{MSG_HANDSHAKE_COMPLETED}")
        return connection

    @staticmethod
    def send_initiate(socket, host, port, message):
        logging.info(f"{MSG_SENDING_INITIATE}")
        Protocol.send_message(socket, host, port, message)
        return

    @staticmethod
    def process_initiate(first_message, client_address, server):
        if first_message.message_type != Message.INITIATE:
            logging.debug(f"{MSG_IS_NOT_INITIATE}")
            exit()
        if client_address in server.clients:
            logging.debug(f"{MSG_CLIENT_ALREADY_HAS_ASSIGNED_CONNECTION}")
            exit()
        logging.debug(f"{MSG_RECEIVED_INITIATE}")
        server.clients.append(client_address)

    @staticmethod
    def sendInack(dedicatedClientSocket, clientAddress, first_message):
        logging.debug(f"{MSG_SENDING_INACK}")

        message = Inack(first_message.transfer_type, first_message.protocol_type)
        message_encoded = message.encode()
        dedicatedClientSocket.sendto(message_encoded, clientAddress)

        logging.debug(f"{MSG_SENT_INACK}")
        return

    @staticmethod
    def receive_inack(socket, host, port):
        message_decoded, server_address = Protocol.receive(socket)

        if message_decoded.message_type != Message.INACK:
            logging.debug(f"{MSG_IS_NOT_INACK}")
            return

        logging.debug(f"{MSG_RECEIVED_INACK}")

        return server_address

    @staticmethod
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

    @staticmethod
    def send_established(socket, host, port, filename):
        logging.info(f"{MSG_SENDING_ESTABLISHED}")
        logging.debug(f"{MSG_FILE_NAME} {filename}")
        message = Established(filename)
        Protocol.send_message(socket, host, port, message)
        return

    @staticmethod
    def decode_received_message(socket: socket):
        recv_buffer, clientAddress = socket.recvfrom(RECV_BUFFER_SIZE)
        fixed_header = recv_buffer[:Message.FIXED_HEADER_SIZE]
        recv_buffer = recv_buffer[Message.FIXED_HEADER_SIZE:]
        message_type = Decoder.decode_fixed_header(fixed_header)
        rest_of_message = recv_buffer
        decoded_message = Decoder.decode_after_fixed_header(message_type, rest_of_message)

        return decoded_message, clientAddress

    @staticmethod
    def decode_message_from_buffer(buffer):
        fixed_header = buffer[:Message.FIXED_HEADER_SIZE]
        message_type = Decoder.decode_fixed_header(fixed_header)
        message_class = MessageClassFactory.create(message_type)
        buffer = buffer[Message.FIXED_HEADER_SIZE:]
        rest_of_message = buffer[:(message_class.MESSAGE_SIZE - Message.FIXED_HEADER_SIZE)]
        decoded_message = Decoder.decode_after_fixed_header(message_type, rest_of_message)
        buffer = buffer[(message_class.MESSAGE_SIZE - Message.FIXED_HEADER_SIZE):]
        return decoded_message, buffer
