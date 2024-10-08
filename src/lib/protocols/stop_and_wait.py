import random
import logging

from lib.protocols.protocol import Protocol
from lib.file_manager import FileManager
import lib.logging_msg as MSG
import lib.constants as CONST
from lib.message import Send, Senack


class StopAndWaitProtocol(Protocol):
    CODE = 0

    @staticmethod
    def uploader_sender_logic(connection, file_path):
        communication_queue = connection.sender_receiver_communication_queue
        thread_manager = connection.thread_manager
        thread_manager.acquire()

        sequence_number = random.randint(1, 1023)
        last_sent_sequence_number = sequence_number
        last_received_ack_number = 0

        file_manager = FileManager(
            CONST.FILE_MODE_READ, file_path, connection.file_name)
        file_chunk = file_manager.read_file_bytes(Send.PAYLOAD_SIZE)

        logging.info(f"{MSG.MSG_SENDING_FILE_USING_STOP_AND_WAIT}")
        while (file_chunk or last_sent_sequence_number !=
               last_received_ack_number):

            message = Send(sequence_number, file_chunk)
            Protocol.send_message(
                connection.socket, connection.destination_host,
                connection.destination_port, message)
            last_sent_sequence_number = sequence_number
            logging.debug(f"{MSG.MSG_SENT_TYPE} {str(message.message_type)} "
                          f"{MSG.MSG_WITH_SEQUENCE_N} "
                          f"{str(message.sequence_number)}")
            thread_manager.notify()
            thread_manager.wait()

            if connection.end_connection_flag.is_set():
                break

            try:
                received_message = communication_queue.pop(0)
            except IndexError:
                logging.debug(f"{MSG.MSG_NO_ACK_RECEIVED}")
                continue

            connection.reset_timer()

            if received_message.ack_number == sequence_number:
                sequence_number += 1
                last_received_ack_number = received_message.ack_number
                file_chunk = file_manager.read_file_bytes(Send.PAYLOAD_SIZE)

        if not file_chunk:
            logging.info(f"{MSG.MSG_FILE_SENT}")
        logging.debug(f"{MSG.MSG_UPLOADER_SENDER_THREAD_ENDING}")
        file_manager.close()
        connection.end_connection_flag.set()
        connection.timeout_timer.cancel()
        thread_manager.release()
        return

    @staticmethod
    def uploader_receiver_logic(connection):
        communication_queue = connection.sender_receiver_communication_queue
        thread_manager = connection.thread_manager

        thread_manager.acquire()
        thread_manager.wait()
        thread_manager.release()

        while True:
            try:
                decoded_message = \
                    Protocol.decode_received_message(connection.socket)[0]
            except TimeoutError:
                connection.wake_up_threads()
                if connection.end_connection_flag.is_set():
                    break
                continue

            thread_manager.acquire()
            logging.debug(f"{MSG.MSG_RECEIVED_MSG_TYPE} "
                          f"{str(decoded_message.message_type)} "
                          f"{MSG.MSG_WITH_ACK_N} "
                          f"{str(decoded_message.ack_number)}")
            communication_queue.append(decoded_message)
            thread_manager.notify()
            thread_manager.release()

        logging.debug(f"{MSG.MSG_UPLOADER_RECEIVER_THREAD_ENDING}")

    @staticmethod
    def downloader_sender_logic(connection):
        communication_queue = connection.sender_receiver_communication_queue
        thread_manager = connection.thread_manager
        thread_manager.acquire()

        while True:
            thread_manager.wait()
            if connection.end_connection_flag.is_set():
                break
            message = communication_queue.pop(0)
            Protocol.send_message(
                connection.socket, connection.destination_host,
                connection.destination_port, message)
            logging.debug(f"{MSG.MSG_SENT_TYPE} "
                          f"{str(message.message_type)} "
                          f"{MSG.MSG_WITH_ACK_N} "
                          f"{str(message.ack_number)}")

        thread_manager.release()
        logging.debug(f"{MSG.MSG_DOWNLOADER_SENDING_THREAD_ENDING}")

    @staticmethod
    def downloader_receiver_logic(connection, storage_path):
        communication_queue = connection.sender_receiver_communication_queue
        thread_manager = connection.thread_manager
        last_sequence_number = 0

        logging.debug(f"{MSG.MSG_STORAGE_PATH} {storage_path}")
        file_manager = FileManager(
            CONST.FILE_MODE_WRITE, storage_path, connection.file_name)
        while connection.end_connection_flag.is_set() is False:
            try:
                decoded_message = \
                    Protocol.decode_received_message(connection.socket)[0]
            except TimeoutError:
                continue

            thread_manager.acquire()
            connection.reset_timer()
            if last_sequence_number == decoded_message.sequence_number - 1 or \
               last_sequence_number == 0:
                file_manager.write_file_bytes(decoded_message.payload)
                logging.debug(f"{MSG.MSG_WRITING_FILE_PATH} "
                              f"{storage_path + connection.file_name}")
            last_sequence_number = decoded_message.sequence_number
            message_ack = Senack(decoded_message.sequence_number)
            communication_queue.append(message_ack)
            thread_manager.notify()
            thread_manager.release()

        file_manager.close()
        logging.debug(f"{MSG.MSG_DOWNLOADER_RECEIVER_THREAD_ENDING}")
