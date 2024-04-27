import socket
from lib.constants import BUFFER_SIZE

class Protocol:
    def __init__(self):
        return

    def send(self, archivo, socket, host, port):
        # Enviamos directamente, no hay handshaking
        socket.sendto(archivo.encode(),(host, port))
        return
    
    def receive(self, socket):
        modifiedMessage, serverAddress = socket.recvfrom(BUFFER_SIZE)
        return modifiedMessage