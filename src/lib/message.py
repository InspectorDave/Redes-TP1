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

    def __init__(self, message_type, transfer_type, packet_number, ack_number, offset, payload):
        self.message_type = message_type
        self.transfer_type = transfer_type
        self.packet_number = packet_number
        self.ack_number = ack_number
        self.offset = offset
        self.payload = payload
        return
    
    # El primer parametro de struct.pack es el formato. Cada I representa
    # un unsigned int de 32 bits, es decir, 4 Bytes y '!' es el formato
    # BIG ENDIAN
    def encode(self):
        header = struct.pack("!BBIII", self.message_type, self.transfer_type, self.packet_number, self.ack_number, self.offset)
        #padding_length = HEADER_SIZE - len(header)
        #if padding_length > 0:
        #    padding = b'\x00' * padding_length
        #    header += padding
        return header + self.payload
    
    @staticmethod
    def decode(data):
        header_data = data[:HEADER_SIZE]
        payload = data[HEADER_SIZE:]
        message_type, transfer_type, packet_number, ack_number, offset = struct.unpack("!BBIII", header_data)
        return Message(message_type, transfer_type, packet_number, ack_number, offset, payload)

class Initiate:
    def __init__(self, transfer_type):
        self.message_type = Message.INITIATE
        self.transfer_type = transfer_type
        return
    
    def encode(self):
        encoded_message = struct.pack("!BB", self.message_type, self.transfer_type)
        return encoded_message
    
    @staticmethod
    def decode(data):
        header_data = data[:2]
        message_type, transfer_type = struct.unpack("!BB", header_data)
        if message_type!=Message.INITIATE:
            raise ValueError("Not an INITIATE")
        return Initiate(transfer_type)
    
class Inack:
    def __init__(self, transfer_type):
        self.message_type = Message.INACK
        self.transfer_type = transfer_type
        return
    
    def encode(self):
        encoded_message = struct.pack("!BB", self.message_type, self.transfer_type)
        return encoded_message
    
    @staticmethod
    def decode(data):
        header_data = data[:2]
        message_type, transfer_type = struct.unpack("!BB", header_data)
        if message_type!=Message.INACK:
            raise ValueError("Not an INACK")
        return Inack(transfer_type)
    
class Send:
    def __init__(self, transfer_type, packet_number, ack_number):
        self.message_type = Message.SEND
        self.transfer_type = transfer_type
        self.packet_number = packet_number
        self.ack_number = ack_number
        return
    
    def encode(self):
        encoded_message = struct.pack("!BBII", self.message_type, self.transfer_type)
        return encoded_message
    
    @staticmethod
    def decode(data):
        header_data = data[:2]
        message_type, transfer_type = struct.unpack("!BBII", header_data)
        if message_type!=Message.INACK:
            raise ValueError("Not an INACK")
        return Inack(transfer_type)
    
class Senack:
    def __init__(self, transfer_type, packet_number, ack_number):
        self.message_type = Message.SENACK
        self.transfer_type = transfer_type
        self.packet_number = packet_number
        self.ack_number = ack_number
        return
    
    def encode(self):
        encoded_message = struct.pack("!BBII", self.message_type, self.transfer_type, self.packet_number, self.ack_number)
        return encoded_message
    
    @staticmethod
    def decode(data):
        header_data = data[:2]
        message_type, transfer_type = struct.unpack("!BBII", header_data)
        if message_type!=Message.INACK:
            raise ValueError("Not an INACK")
        return Inack(transfer_type)