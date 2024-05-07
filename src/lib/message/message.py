from lib.constants import *
import struct
import random

# El header (compuesto por packet_number y ack_number) debe ser
# menor que el HEADER_SIZE

# IMPORTANTE: Al agregar un campo al header 
# hay que modificar la funcion encode() y decode() y HEADER_SIZE
class Message:

    INITIATE = 0
    INACK = 1
    SEND = 2
    SENACK = 3

    def __init__(self, message_type, transfer_type, protocol_type, packet_number, ack_number, payload):
        self.message_type = message_type
        self.transfer_type = transfer_type
        self.protocol_type = protocol_type
        self.packet_number = packet_number
        self.ack_number = ack_number
        self.payload = payload
        return
    
    # El primer parametro de struct.pack es el formato. Cada I representa
    # un uint32, cada B un uint8, y '!' es el formato BIG ENDIAN
    def encode(self):
        header = struct.pack("!BBBII", self.message_type, 
                            self.transfer_type,
                            self.protocol_type,
                            self.packet_number,
                            self.ack_number)
        return header + self.payload
    
    @staticmethod
    def decode(data):
        header_data = data[:HEADER_SIZE]
        payload = data[HEADER_SIZE:]
        message_type, transfer_type, protocol_type, packet_number, \
            ack_number = struct.unpack("!BBBII", header_data)
        return Message(message_type, transfer_type, protocol_type, packet_number, ack_number, payload)
    
    def get_payload(self):
        return self.payload
