from socket import *
from lib.constants import BUFFER_SIZE
from lib.message import *
from lib.protocols.protocol import *
from lib.protocols.stop_and_wait import *
from lib.protocols.go_back_n import *

class Client:
    def __init__(self, server_host, server_port, args, transfer_type):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(AF_INET, SOCK_DGRAM)
        self.file_name = args.name
        if (args.protocol == 's'):
            self.protocol = StopAndWaitProtocol() # Pasarlo por parametro al ejecutar
        elif (args.protocol == 'g'):
            self.protocol = GoBackNProtocol()
        else:
            logging.error(f"Error al crear el cliente")
        self.transfer_type = transfer_type
        self.keep_alive_timer = Timer(KEEP_ALIVE, end_process, (self, ))
        self.end_process = Event()
        self.thread_manager = Condition()

    def start(self):
        self.socket.settimeout(TIME_OUT)
        new_server_address = self.protocol.perform_client_side_handshake(self)
        self.server_host, self.server_port = new_server_address
        return

    def upload(self, file_path, filename):
        
        communication_queue = []

        thread_receiver = Thread(target=self.protocol.uploader_receiver_logic, args=(self, self.thread_manager, communication_queue))
        thread_receiver.start()
    
        thread_sender = Thread(target=self.protocol.uploader_sender_logic, args=(self, file_path, filename, self.thread_manager, communication_queue))
        thread_sender.start()
        return
    
    def download(self):
        complete_file = self.protocol.receive_file(socket)
        return complete_file
    
    def close_socket():
        socket.shutdown(SHUT_RDWR)
        socket.close()
        return
    
    def reset_timer(self):
        self.keep_alive_timer.cancel()
        self.keep_alive_timer = Timer(KEEP_ALIVE, end_process, (self,))
        self.keep_alive_timer.start()
        return
    
def end_process(client):
    logging.info(f"{MSG_KEEP_ALIVE_TIMEOUT}")
    client.keep_alive_timer.cancel()
    client.end_process.set()
    return
