from lib.protocols.protocol import *
import random
from threading import *

class StopAndWaitProtocol(Protocol):

    def uploader_sender_logic(self, file_path, client_socket:socket.socket, host, port, thread_manager, communication_queue):
        print("Sending file using Stop and Wait Protocol")

        message_type = Message.SEND
        transfer_type = Protocol.UPLOAD
        protocol_type = Protocol.STOP_AND_WAIT

        sequence_number = random.randint(1, 1023)

        file_manager = FileManager(FILE_MODE_READ, file_path)
        file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        while file_chunk:
            message = Message(message_type, transfer_type,protocol_type, sequence_number, self.ack_number, self.offset, file_chunk)
            sent = self.send_message(client_socket, host, port, message)
            
            self.offset += len(file_chunk)
            self.packet_number += 1
            self.ack_number += 1
            print(f"[LOG] {sent} bytes sent")
            file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        file_manager.close()

    def uploader_receiver_logic(self, client_socket:socket.socket, thread_manager, communication_queue):
        while True:
            a = 0 #

    def downloader_sender_logic(self, client_socket:socket.socket, thread_manager, communication_queue):

        # sequence_number = random.randint(1, 1023)

        while True:
            a = 0 #para que ande el while true

    def downloader_receiver_logic(self,client_socket:socket.socket, thread_manager, communication_queue):

        ack_number = 0

        while True:
            message, clientAddress = client_socket.recvfrom(BUFFER_SIZE)
            decoded_message = Message.decode(message)

            # print("[LOG] Client Address: ", clientAddress)
            print("[LOG] Received message type: ", decoded_message.message_type)
            print("[LOG] Bytes recibidos: ", len(message))
            # print("[LOG] Bytes recibidos: ", decoded_message.payload)
            print("[LOG] Processed existing connection.")