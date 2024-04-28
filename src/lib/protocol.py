import socket
from lib.constants import BUFFER_SIZE

class Protocol:
    def __init__(self):
        return

    def send(self, file_content, socket, host, port):
        # Enviamos directamente, no hay handshaking
        print(type(file_content))
        socket.sendto(file_content,(host, port))
        return
    
    def receive(self, socket):
        modifiedMessage, serverAddress = socket.recvfrom(BUFFER_SIZE)
        return modifiedMessage