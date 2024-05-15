from threading import Event, Timer
import logging

from lib.protocols.protocol import Protocol
from lib.file_manager import FileManager, FILE_MODE_READ, FILE_MODE_WRITE
import lib.logging_msg as MSG
import lib.constants as CONST
from lib.message import Send, Senack


class GoBackN(Protocol):
    CODE = 1

    @staticmethod
    def uploader_sender_logic(connection, file_path):
        communication_queue = connection.sender_receiver_communication_queue
        thread_manager = connection.thread_manager
        thread_manager.acquire()

        last_sent_sequence_number = 1   # random.randint(1, 1023)

        file_manager = FileManager(
            FILE_MODE_READ, file_path, connection.file_name)
        file_chunk = file_manager.read_file_bytes(Send.PAYLOAD_SIZE)
        messages_not_ackd = []

        resend_window_flag = Event()
        resend_window_timer = Timer(
            CONST.TIME_OUT, GoBackN.resend_window_timer,
            args=(resend_window_flag,))
        resend_window_timer.start()

        thread_manager.notify()

        logging.info(f"{MSG.MSG_SENDING_FILE_USING_GO_BACK_N}")

        while file_chunk or len(messages_not_ackd) != 0:
            while file_chunk and len(messages_not_ackd) < CONST.WINDOW_SIZE:

                message = Send(last_sent_sequence_number, file_chunk)

                Protocol.send_message(
                    connection.socket,
                    connection.destination_host,
                    connection.destination_port,
                    message)
                logging.debug(f"{MSG.MSG_SENT_TYPE} "
                              f"{str(message.message_type)} "
                              f"{MSG.MSG_WITH_SEQUENCE_N} "
                              f"{str(message.sequence_number)}")

                messages_not_ackd.append(message)
                last_sent_sequence_number += 1
                file_chunk = file_manager.read_file_bytes(Send.PAYLOAD_SIZE)

            if resend_window_flag.is_set():
                logging.debug(f"{MSG.MSG_RESENDING_WINDOW}")
                for message in messages_not_ackd:
                    Protocol.send_message(connection.socket,
                                          connection.destination_host,
                                          connection.destination_port,
                                          message)
                    logging.debug(f"{MSG.MSG_SENT_TYPE} "
                                  f"{str(message.message_type)} "
                                  f"{MSG.MSG_WITH_SEQUENCE_N} "
                                  f"{str(message.sequence_number)}")

                resend_window_flag.clear()
                GoBackN.reset_timer(resend_window_timer, resend_window_flag)

            thread_manager.wait()

            if connection.end_connection_flag.is_set():
                break

            while len(communication_queue) > 0:
                received_message = communication_queue.pop(0)
                connection.reset_timer()
                while (len(messages_not_ackd) > 0 and
                       received_message.ack_number >=
                       messages_not_ackd[0].sequence_number):
                    if received_message.ack_number ==\
                       messages_not_ackd[0].sequence_number:
                        GoBackN.reset_timer(resend_window_timer,
                                            resend_window_flag)
                    messages_not_ackd.pop(0)

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
            # if connection.end_connection_flag.is_set():
            #     break
            try:
                buffer = connection.socket.recvfrom(CONST.RECV_BUFFER_SIZE)[0]
            except TimeoutError:
                connection.wake_up_threads()
                if connection.end_connection_flag.is_set():
                    break
                continue
            thread_manager.acquire()
            while len(buffer) > 0:
                # if connection.end_connection_flag.is_set():
                #     break
                connection.reset_timer()
                decoded_message, buffer = \
                    Protocol.decode_message_from_buffer(buffer)
                logging.debug(
                    f"{MSG.MSG_RECEIVED_MSG_TYPE} "
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
            while len(communication_queue) > 0:
                message = communication_queue.pop(0)
                Protocol.send_message(connection.socket,
                                      connection.destination_host,
                                      connection.destination_port,
                                      message)
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
        file_manager = FileManager(FILE_MODE_WRITE, storage_path,
                                   connection.file_name)
        while connection.end_connection_flag.is_set() is False:
            try:
                buffer, clientAddress = connection.socket.recvfrom(
                    Send.MESSAGE_SIZE * CONST.WINDOW_SIZE * 2)
                thread_manager.acquire()
                connection.reset_timer()
                while len(buffer) > 0:
                    decoded_message, buffer = \
                        Protocol.decode_message_from_buffer(buffer)
                    logging.debug(
                        f"{MSG.MSG_RECEIVED_MSG_TYPE} "
                        f"{str(decoded_message.message_type)} "
                        f"{MSG.MSG_WITH_SEQUENCE_N} "
                        f"{str(decoded_message.sequence_number)}")
                    if last_sequence_number == \
                       decoded_message.sequence_number - 1\
                       or last_sequence_number == 0:
                        file_manager.write_file_bytes(decoded_message.payload)
                        logging.debug(f"{MSG.MSG_WRITING_FILE_PATH} "
                                      f"{storage_path + connection.file_name}")
                        last_sequence_number = decoded_message.sequence_number
                    message_ack = Senack(last_sequence_number)
                    communication_queue.append(message_ack)
                thread_manager.notify()
                thread_manager.release()
            except TimeoutError:
                continue

        file_manager.close()
        logging.debug(f"{MSG.MSG_DOWNLOADER_RECEIVER_THREAD_ENDING}")

    @staticmethod
    def resend_window_timer(resend_window_flag):
        resend_window_flag.set()
        return

    @staticmethod
    def reset_timer(timer, resend_window_flag):
        timer.cancel()
        timer = Timer(CONST.TIME_OUT, GoBackN.resend_window_timer,
                      args=(resend_window_flag,))
        timer.start()
