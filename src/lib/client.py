from socket import *
from lib.constants import BUFFER_SIZE
from lib.message import *
from lib.protocol import Protocol
from lib.file_manager import *
from lib.file_manager import *

class Client:
    def __init__(self, host, port, args):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.protocol = Protocol()

    def start(self):

        self.perform_handshake()

        # Creamos el Socket
        #clientSocket = socket(AF_INET, SOCK_DGRAM)
        # Habria que crear el socket de transferencia, este es el de conexion
        #message = ' '
        #while message.upper() != 'FIN' :
        #    message = input("Input lowercase sentence:")
        #    self.upload(message, clientSocket)
        #    complete_file = self.download(clientSocket)
        #    print(complete_file.decode())

        # Cerramos
        #clientSocket.close()
        return

    def upload(self, file_path):
        # file_manager = FileManager()
        # file_content = file_manager.read_file_bytes(file_path)
        # self.protocol.send(file_content, self.socket, self.host, self.port)
        return
    
    def download(self):
        complete_file = self.protocol.receive(socket)
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
        message = Initiate(Protocol.UPLOAD)
        message_bytes = message.encode()
        self.socket.sendto(message_bytes, (self.host, self.port))
        return
    
    def receive_inack(self):
        message, serverAddress = self.socket.recvfrom(BUFFER_SIZE)
        message_decoded = Inack.decode(message)

        if message_decoded.message_type != Message.INACK:
            print("[LOG] Message isn't Inack")
            return

        print("[LOG] Received an Inack")

        self.host = serverAddress[0]
        self.port = serverAddress[1]

        return

    def send_senack(self):
        print("[LOG] Sending SENACK")
        message = Senack(Protocol.UPLOAD, random.randint(0, 1000), 0)
        message_bytes = message.encode()
        self.socket.sendto(message_bytes, (self.host, self.port))
        return