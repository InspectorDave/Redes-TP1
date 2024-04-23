from socket import *

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        

    #Defino Port
#    serverPort = 12000
    #Defino IP4v y UDP
#    serverSocket = socket(AF_INET, SOCK_DGRAM)
#    serverSocket.bind(('', serverPort))
#    print("The server is ready to receive")
#    while True:
        # Se recibe directamente, no hay pasos previos como "accept" o "listen" para el handshaking
#        message, clientAddress = serverSocket.recvfrom(2048)
        # Tomo Client Address, vean que Port imprime:
#        print ("Client Address: ", clientAddress)
#        modifiedMessage = message.decode().upper()
#        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
#        print ("Message sent")
#        if modifiedMessage == "FIN":
#            break
#        serverSocket.close()