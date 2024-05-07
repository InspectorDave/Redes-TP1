from lib.protocols.protocol import *
import random
from threading import *
import logging

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
            logging.debug(f"[LOG] Sent message type {str(message.message_type)} , with sequence {str(message.packet_number)}" )
            logging.debug(f"[LOG] {sent} bytes sent")
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
        thread_manager.release()

        while True:
            message, clientAddress = socket.recvfrom(BUFFER_SIZE)
            thread_manager.acquire()
            decoded_message = Message.decode(message)
            logging.debug(f"[LOG] Received message type {str(decoded_message.message_type)}, with ACK {str(decoded_message.ack_number)}" )
            communication_queue.append(decoded_message)
            thread_manager.notify()
            thread_manager.release()

    def downloader_sender_logic(self, socket:socket.socket, host, port, thread_manager, communication_queue):
        thread_manager.acquire()

        while True:
            thread_manager.wait()
            message = communication_queue.pop(0)
            sent = self.send_message(socket, host, port, message)
            logging.debug(f"[LOG] Sent message type {str(message.message_type)}, with ACK {str(message.ack_number)}")

    def downloader_receiver_logic(self,socket:socket.socket, thread_manager, communication_queue):
        last_packet_number = 0
        ack_number = 0

        while True:
            message, clientAddress = socket.recvfrom(BUFFER_SIZE)
            thread_manager.acquire()
            decoded_message = Message.decode(message)

            logging.debug(f"[LOG] Received message type: {decoded_message.message_type}, with sequence {decoded_message.packet_number}")
            logging.debug(f"[LOG] Bytes recibidos: {len(message)}")
            # print("[LOG] Bytes recibidos: ", decoded_message.payload)

            if last_packet_number == decoded_message.packet_number - 1:
                # Acá debería estar la lógica de guardar en un archivo lo recibido.
                # A este if se entra si el paquete recibido no está repetido, si no
                # se escribirían en el archivo 2 veces los paquetes que sabemos que están repetidos.
                BORRAR = 0 # Esto está acá para que compile nomás :)

            last_packet_number = decoded_message.packet_number

            message_type = Message.SENACK
            transfer_type = Protocol.UPLOAD
            protocol_type = Protocol.STOP_AND_WAIT
            ack_number = decoded_message.packet_number + 1
            message_ack = Message(message_type, transfer_type, protocol_type, 0, ack_number, 0, b'')

            communication_queue.append(message_ack)
            thread_manager.notify()
            thread_manager.release()
