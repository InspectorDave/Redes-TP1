import random
from threading import *
import logging
from socket import *

from lib.protocols.protocol import Protocol
from lib.file_manager import FileManager
from lib.logging_msg import *
from lib.constants import *
from lib.message import Send, Senack

class StopAndWaitProtocol(Protocol):
    CODE = 0

    def uploader_sender_logic(self, connection, file_path, filename, communication_queue):
        logging.info(f"{MSG_SENDING_FILE_USING_STOP_AND_WAIT}")
        
        thread_manager = connection.thread_manager
        thread_manager.acquire()

        sequence_number = random.randint(1, 1023)

        file_manager = FileManager(FILE_MODE_READ, file_path, filename)
        file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        
        while file_chunk:

            message = Send(sequence_number, file_chunk)
            sent = self.send_message(connection.socket, connection.server_host, connection.server_port, message)
            logging.debug(f"{MSG_SENT_TYPE} {str(message.message_type)} {MSG_WITH_SEQUENCE_N} {str(message.sequence_number)}" )
            logging.debug(f"{MSG_BYTES_SENT} {sent}")
            thread_manager.notify()
            thread_manager.wait()

            if connection.end_connection_flag.is_set():
                break

            try:
                received_message = communication_queue.pop(0)
            except IndexError:
                logging.debug(f"{MSG_NO_ACK_RECEIVED}")
                continue

            connection.reset_timer()

            if received_message.ack_number == sequence_number + 1:
                sequence_number += 1
                file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)

        logging.debug(f"{MSG_UPLOADER_SENDER_THREAD_ENDING}")
        file_manager.close()
        connection.end_connection_flag.set()
        connection.keep_alive_timer.cancel()
        thread_manager.release()
        return

    def uploader_receiver_logic(self, connection, communication_queue):

        thread_manager = connection.thread_manager

        thread_manager.acquire()
        thread_manager.wait()
        thread_manager.release()

        while True:
            try:
                decoded_message, downloader_address = self.decode_received_message(connection.socket)
            except TimeoutError:
                self.wake_up_threads(thread_manager)
                if connection.end_connection_flag.is_set():
                    break
                continue

            thread_manager.acquire()
            logging.debug(f"{MSG_RECEIVED_MSG_TYPE} {str(decoded_message.message_type)} {MSG_WITH_ACK_N} {str(decoded_message.ack_number)}" )
            communication_queue.append(decoded_message)
            thread_manager.notify()
            thread_manager.release()

        logging.debug(f"{MSG_UPLOADER_RECEIVER_THREAD_ENDING}")

    def downloader_sender_logic(self, socket:socket, host, port, thread_manager:Condition, communication_queue:list):
        thread_manager.acquire()

        while True:
            thread_manager.wait()
            message = communication_queue.pop(0)
            self.send_message(socket, host, port, message)
            logging.debug(f"{MSG_SENT_TYPE} {str(message.message_type)} {MSG_WITH_ACK_N} {str(message.ack_number)}")

    def downloader_receiver_logic(self,socket:socket, thread_manager, communication_queue, storage_path, file_name):

        logging.info(f"Downloader receiver logic socket: {socket}")

        last_sequence_number = 0
        ack_number = 0
        logging.debug(f"{MSG_STORAGE_PATH} {storage_path}")
        file_manager = FileManager(FILE_MODE_WRITE, storage_path, file_name)
        while True:
            try: #Para poder hacer que se cierre el archivo en el finally
                decoded_message, client_address = self.decode_received_message(socket)
                thread_manager.acquire()
                if last_sequence_number == decoded_message.sequence_number - 1 or last_sequence_number == 0:
                    file_manager.write_file_bytes(decoded_message.payload)
                    logging.debug(f"{MSG_WRITING_FILE_PATH} {storage_path+file_name}")
                last_sequence_number = decoded_message.sequence_number
                message_ack = Senack(decoded_message.sequence_number + 1)
                communication_queue.append(message_ack)
                thread_manager.notify()
                thread_manager.release()
            except Exception as e:
                raise Exception(f"Error: {e}")
            #finally:
                #print("CLOSING FILE")
                #print("FILE: ", file_manager.file)
                #file_manager.close()

    def wake_up_threads(self, thread_manager):
        thread_manager.acquire()
        thread_manager.notify()
        thread_manager.release()
        return
