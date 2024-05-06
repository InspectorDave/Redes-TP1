from lib.protocols.protocol import *
import random
from threading import *

class StopAndWaitProtocol(Protocol):

    def uploader_sender_logic(self, file_path, socket:socket.socket, host, port, thread_manager, communication_queue):
        print("Sending file using Stop and Wait Protocol")
        thread_manager.acquire()
        message_type = Message.SEND
        transfer_type = Protocol.UPLOAD
        protocol_type = Protocol.STOP_AND_WAIT

        sequence_number = random.randint(1, 1023)

        file_manager = FileManager(FILE_MODE_READ, file_path)
        file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        while file_chunk:
            message = Message(message_type, transfer_type,protocol_type, sequence_number, self.ack_number, self.offset, file_chunk)
            sent = self.send_message(socket, host, port, message)
            print(f"[LOG] {sent} bytes sent")
            thread_manager.notify()
            thread_manager.wait()

            received_message = communication_queue.pop(0)

            if received_message.ack_number == sequence_number + 1:
                self.offset += len(file_chunk)
                sequence_number += 1
                self.ack_number += 1
                file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)

        file_manager.close()

    def uploader_receiver_logic(self, socket:socket.socket, thread_manager, communication_queue):
        thread_manager.acquire()
        thread_manager.wait()
        while True:
            thread_manager.acquire()
            message, clientAddress = socket.recvfrom(BUFFER_SIZE)
            decoded_message = Message.decode(message)
            communication_queue.push(decoded_message)
            thread_manager.notify()

    def downloader_sender_logic(self, socket:socket.socket, thread_manager, communication_queue):

        # sequence_number = random.randint(1, 1023)

        while True:
            a = 0 #para que ande el while true

    def downloader_receiver_logic(self,socket:socket.socket, thread_manager, communication_queue):

        ack_number = 0

        while True:
            message, clientAddress = socket.recvfrom(BUFFER_SIZE)
            decoded_message = Message.decode(message)

            # print("[LOG] Client Address: ", clientAddress)
            print("[LOG] Received message type: ", decoded_message.message_type)
            print("[LOG] Bytes recibidos: ", len(message))
            # print("[LOG] Bytes recibidos: ", decoded_message.payload)
            print("[LOG] Processed existing connection.")
