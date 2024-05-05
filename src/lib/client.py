from socket import *
from lib.constants import BUFFER_SIZE
from lib.message import *
from lib.protocol import Protocol

class Client:
    def __init__(self, host, port, args):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.protocol = Protocol()

    def start(self):

        self.perform_handshake()
        return

    def upload(self, file_path):
        self.protocol.send_file(file_path, self.socket, self.host, self.port)
        return
    
    def download(self):
        complete_file = self.protocol.receive_file(socket)
        return complete_file
    
    def close_socket():
        socket.close()
        return

    def perform_handshake(self):
        print("[LOG] Handshake starting...")
        self.send_initiate()
        self.receive_inack()
        self.send_senack()
        print("[LOG] Handshake completed")
        return

    def send_initiate(self):
        print("[LOG] Sending INITIATE")
        message = Message(Message.INITIATE, Protocol.UPLOAD, Protocol.STOP_AND_WAIT, 0, 0, 0, b'')
        message_bytes = message.encode()
        self.socket.sendto(message_bytes, (self.host, self.port))
        return
    
    def receive_inack(self):
        message, serverAddress = self.socket.recvfrom(BUFFER_SIZE)
        message_decoded = Message.decode(message)

        if message_decoded.message_type != Message.INACK:
            print("[LOG] Message isn't Inack")
            return

        print("[LOG] Received an Inack")

        self.host = serverAddress[0]
        self.port = serverAddress[1]

        return

    def send_senack(self):
        print("[LOG] Sending SENACK")
        message = Message(Message.SENACK, Protocol.UPLOAD,Protocol.STOP_AND_WAIT, 0, 0, 0, b'')
        message_encoded = message.encode()
        self.socket.sendto(message_encoded, (self.host, self.port))
        return