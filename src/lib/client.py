from socket import *
from lib.constants import BUFFER_SIZE
from lib.message import *
from lib.protocols.protocol import *
from lib.protocols.stop_and_wait import *
from lib.protocols.go_back_n import *

class Client:
    def __init__(self, server_host, server_port, args):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(AF_INET, SOCK_DGRAM)
        if (args.protocol == 's'):
            self.protocol = StopAndWaitProtocol() # Pasarlo por parametro al ejecutar
        elif (args.protocol == 'g'):
            self.protocol = GoBackNProtocol()
        else:
            raise ValueError("Error al crear el cliente")

    def start(self):
        new_server_address = self.protocol.perform_client_side_handshake(self.socket, self.server_host, self.server_port)
        self.server_host, self.server_port = new_server_address
        return

    def upload(self, file_path):

        thread_manager = Condition()
        communication_queue = []

        thread_receiver = Thread(target=self.protocol.uploader_receiver_logic, args=(self.socket, thread_manager, communication_queue))
        thread_receiver.start()
    
        thread_sender = Thread(target=self.protocol.uploader_sender_logic, args=(file_path, self.socket, self.server_host, self.server_port, thread_manager, communication_queue))
        thread_sender.run()
        return
    
    def download(self):
        complete_file = self.protocol.receive_file(socket)
        return complete_file
    
    def close_socket():
        socket.close()
        return
