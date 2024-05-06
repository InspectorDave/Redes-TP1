from lib.protocols.protocol import *

class StopAndWaitProtocol(Protocol):

    def send_file(self, file_path, client_socket, host, port):
        print("Sending file using Stop and Wait Protocol")

        message_type = Message.SEND
        transfer_type = Protocol.UPLOAD
        protocol_type = Protocol.STOP_AND_WAIT
        file_manager = FileManager(FILE_MODE_READ, file_path)
        file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        while file_chunk:
            message = Message(message_type, transfer_type,protocol_type, self.packet_number, self.ack_number, self.offset, file_chunk)
            sent = self.send_message(client_socket, host, port, message)
            self.offset += len(file_chunk)
            self.packet_number += 1
            self.ack_number += 1
            print(f"[LOG] {sent} bytes sent")
            file_chunk = file_manager.read_file_bytes(PAYLOAD_SIZE)
        file_manager.close()        

    def receive_file(self,client_socket:socket.socket):
        print("Receiving file using Stop and Wait Protocol")
        # file_manager = FileManager(FILE_MODE_WRITE, DEFAULT_SERVER_STORAGE)
        # file_manager.open_to_write(DEFAULT_SERVER_STORAGE)

        while True:
            message, clientAddress = client_socket.recvfrom(BUFFER_SIZE)
            decoded_message = Message.decode(message)
            # print("[LOG] Client Address: ", clientAddress)
            print("[LOG] Received message type: ", decoded_message.message_type)
            print("[LOG] Bytes recibidos: ", len(message))
            # print("[LOG] Bytes recibidos: ", decoded_message.payload)
            print("[LOG] Processed existing connection.")

        #file_manager.close()
