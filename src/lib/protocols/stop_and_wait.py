from lib.protocols.protocol import *
import random
from threading import *
import logging
import time

class StopAndWaitProtocol(Protocol):

    def uploader_sender_logic(self, file_path, filename, socket:socket.socket, host, port, thread_manager:Condition, communication_queue, stop_thread):
        print("Sending file using Stop and Wait Protocol")
        thread_manager.acquire()
        message_type = Message.SEND
        transfer_type = Protocol.UPLOAD
        protocol_type = Protocol.STOP_AND_WAIT

        sequence_number = random.randint(1, 1023)
        offset = 0

        file_manager = FileManager(FILE_MODE_READ, file_path, filename)
        file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)

        while file_chunk:
            message = Message(message_type, transfer_type,protocol_type, sequence_number, 0, offset, file_chunk)
            sent = self.send_message(socket, host, port, message)
            logging.debug(f"[LOG] Sent message type {str(message.message_type)} , with sequence {str(message.packet_number)}" )
            logging.debug(f"[LOG] {sent} bytes sent")
            thread_manager.notify()
            thread_manager.wait()

            try:
                received_message = communication_queue.pop(0)
            except IndexError:
                logging.debug(f"[LOG] No ACK received")
                continue

            if received_message.ack_number == sequence_number + 1:
                offset += len(file_chunk)
                sequence_number += 1
                file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)

        file_manager.close()
        stop_thread.set()
        thread_manager.release()
        return

    def uploader_receiver_logic(self, socket:socket.socket, thread_manager:Condition, communication_queue, stop_thread):
        thread_manager.acquire()
        thread_manager.wait()
        thread_manager.release()

        while True:
            try:
                message, clientAddress = socket.recvfrom(BUFFER_SIZE)
            except:
                if stop_thread.is_set():
                    break
                self.wake_up_threads(thread_manager)
                continue

            thread_manager.acquire()
            decoded_message = Message.decode(message)
            logging.debug(f"[LOG] Received message type {str(decoded_message.message_type)}, with ACK {str(decoded_message.ack_number)}" )
            communication_queue.append(decoded_message)
            thread_manager.notify()
            thread_manager.release()

    def downloader_sender_logic(self, socket:socket.socket, host, port, thread_manager:Condition, communication_queue:list):
        thread_manager.acquire()

        while True:
            thread_manager.wait()
            message = communication_queue.pop(0)
            sent = self.send_message(socket, host, port, message)
            logging.debug(f"[LOG] Sent message type {str(message.message_type)}, with ACK {str(message.ack_number)}")

    def downloader_receiver_logic(self,socket:socket.socket, thread_manager, communication_queue, storage_path):
        last_packet_number = 0
        ack_number = 0
        print("STORAGE_PATH ", storage_path)
        file_manager = FileManager(FILE_MODE_WRITE, storage_path, DEFAULT_FILE_NAME)
        while True:
            try: #Para poder hacer que se cierre el archivo en el finally
                message, clientAddress = socket.recvfrom(BUFFER_SIZE)
                thread_manager.acquire()
                decoded_message = Message.decode(message)

                logging.debug(f"[LOG] Received message type: {decoded_message.message_type}, with sequence {decoded_message.packet_number}")
                logging.debug(f"[LOG] Bytes recibidos: {len(message)}")
                # print("[LOG] Bytes recibidos: ", decoded_message.payload)

                if last_packet_number == decoded_message.packet_number - 1 or last_packet_number == 0:
                    file_manager.write_file_bytes(decoded_message.payload)
                    #print("PAYLOAD: ",decoded_message.payload)
                    print("[LOG] Writing file in ", storage_path+DEFAULT_FILE_NAME)

                last_packet_number = decoded_message.packet_number

                message_type = Message.SENACK
                transfer_type = Protocol.UPLOAD
                protocol_type = Protocol.STOP_AND_WAIT
                ack_number = decoded_message.packet_number + 1
                message_ack = Message(message_type, transfer_type, protocol_type, 0, ack_number, 0, b'')

                communication_queue.append(message_ack)
                thread_manager.notify()
                thread_manager.release()
            except Exception as e:
                print(f"Error: {e}")
            #finally:
                #print("CLOSING FILE")
                #print("FILE: ", file_manager.file)
                #file_manager.close()

    def wake_up_threads(self, thread_manager):
        thread_manager.acquire()
        thread_manager.notify()
        thread_manager.release()
        return