from socket import *
from lib.constants import BUFFER_SIZE
from lib.message import *
from lib.protocols.protocol import *
from lib.protocols.stop_and_wait import *
from lib.protocols.go_back_n import *

class Client:
    def __init__(self, server_host, server_port, transfer_type, args):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(AF_INET, SOCK_DGRAM)
        self.file_name = args.name
        self.transfer_type = transfer_type
        if (args.protocol == STOP_AND_WAIT):
            self.protocol = StopAndWaitProtocol() # Pasarlo por parametro al ejecutar
            self.protocol_n = STOP_AND_WAIT_N
        elif (args.protocol == GO_BACK_N):
            self.protocol = GoBackNProtocol()
            self.protocol_n = GO_BACK_N_N
        else:
            logging.error(f"{MSG_CLIENT_CREATION_ERROR}")
            raise ValueError(f"{MSG_CLIENT_CREATION_ERROR}")

    def start(self):
        self.socket.settimeout(TIME_OUT)
        new_server_address = self.protocol.perform_client_side_handshake(self.socket, self.server_host, self.server_port, self.file_name, self.transfer_type, self.protocol_n)
        self.server_host, self.server_port = new_server_address
        return

    def upload(self, file_path, filename):
        
        thread_manager = Condition()
        communication_queue = []
        stop_thread = Event()

        thread_receiver = Thread(target=self.protocol.uploader_receiver_logic, args=(self.socket, thread_manager, communication_queue, stop_thread))
        thread_receiver.start()
    
        thread_sender = Thread(target=self.protocol.uploader_sender_logic, args=(file_path, filename, self.socket, self.server_host, self.server_port, thread_manager, communication_queue, stop_thread))
        thread_sender.start()
        return
    
    def download(self):
        complete_file = self.protocol.receive_file(socket)
        return complete_file
    
    def close_socket():
        socket.shutdown(SHUT_RDWR)
        socket.close()
        return
