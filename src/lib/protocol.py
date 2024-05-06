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
        raise NotImplementedError("send_file method must be implemented in subclass")
    
    # Se encarga de recibir el archivo e ir escribiendolo
    def receive_file(self,client_socket:socket.socket):
        raise NotImplementedError("receive_file method must be implemented in subclass")

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
        print("[LOG] Handshake starting...")
        self.send_initiate(socket, host, port)
        comm_server_address = self.receive_inack(socket, host, port)
        self.send_senack(socket, comm_server_address[0], comm_server_address[1])
        print("[LOG] Handshake completed")
        return comm_server_address

    def send_initiate(self, socket, host, port):
        print("[LOG] Sending INITIATE")
        message = Message(Message.INITIATE, Protocol.UPLOAD, Protocol.STOP_AND_WAIT, 0, 0, 0, b'')
        self.send_message(socket, host, port, message)
        return
    
    def receive_inack(self, socket, host, port):
        message_decoded, server_address = self.receive(socket)

        if message_decoded.message_type != Message.INACK:
            print("[LOG] Message isn't Inack")
            return

        print("[LOG] Received an Inack")

        return server_address

    def send_senack(self, socket, host, port):
        print("[LOG] Sending SENACK")
        message = Message(Message.SENACK, Protocol.UPLOAD,Protocol.STOP_AND_WAIT, 0, 0, 0, b'')
        self.send_message(socket, host, port, message)
        return
    
class StopAndWaitProtocol(Protocol):

    def send_file(self, file_path, client_socket, host, port):
        message_type = Message.SEND
        transfer_type = Protocol.UPLOAD
        protocol_type = Protocol.STOP_AND_WAIT
        file_manager = FileManager(FILE_MODE_READ, file_path)
        file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        while file_chunk:
            message = Message(message_type, transfer_type,protocol_type, self.packet_number, self.ack_number, self.offset, file_chunk)
            sent = self.send_message(client_socket, host, port, message)
            self.offset += len(file_chunk)
            self.packet_number += 1
            self.ack_number += 1
            print(f"[LOG] {sent} bytes sent")
            file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        file_manager.close()        
        print("Sending file using Stop and Wait Protocol")

    def receive_file(self,client_socket:socket.socket):
        file_manager = FileManager(FILE_MODE_WRITE, DEFAULT_SERVER_STORAGE)
        file_manager.open_to_write(DEFAULT_SERVER_STORAGE)
        #while (not conection_finalized):
        #    message_recv = self.receive(client_socket)
        #    file_manager.write_file_bytes(message_recv.get_payload())
        file_manager.close()
        print("Receiving file using Stop and Wait Protocol")

class GoBackNProtocol(Protocol):

    def send_file(self, file_path, client_socket, host, port):
        message_type = Message.SEND
        transfer_type = Protocol.UPLOAD
        protocol_type = Protocol.GO_BACK_N
        file_manager = FileManager(FILE_MODE_READ, file_path)
        file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        while file_chunk:
            message = Message(message_type, transfer_type,protocol_type, self.packet_number, self.ack_number, self.offset, file_chunk)
            sent = self.send_message(client_socket, host, port, message)
            self.offset += len(file_chunk)
            self.packet_number += 1
            self.ack_number += 1
            print(f"[LOG] {sent} bytes sent")
            file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        file_manager.close()
        print("Sending file using Go-Back-N Protocol")

    def receive_file(self,client_socket:socket.socket):
        file_manager = FileManager(FILE_MODE_WRITE, DEFAULT_SERVER_STORAGE)
        file_manager.open_to_write(DEFAULT_SERVER_STORAGE)
        #while (not conection_finalized):
        #    message_recv = self.receive(client_socket)
        #    file_manager.write_file_bytes(message_recv.get_payload())
        file_manager.close()
        print("Receiving file using Go-Back-N Protocol")
