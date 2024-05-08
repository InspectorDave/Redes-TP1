from lib.constants import *
import struct
import random

# El header (compuesto por packet_number y ack_number) debe ser
# menor que el HEADER_SIZE

# IMPORTANTE: Al agregar un campo al header 
# hay que modificar la funcion encode() y decode() y HEADER_SIZE
class Message:
    FIXED_HEADER_SIZE = 1

    INITIATE = 0
    INACK = 1
    SEND = 2
    SENACK = 3
    ESTABLISHED = 4

    # def __init__(self, message_type, transfer_type, protocol_type, packet_number, ack_number, payload):
    #     self.message_type = message_type
    #     self.transfer_type = transfer_type
    #     self.protocol_type = protocol_type
    #     self.packet_number = packet_number
    #     self.ack_number = ack_number
    #     self.payload = payload
    #     return
    
    # El primer parametro de struct.pack es el formato. Cada I representa
    # un uint32, cada B un uint8, y '!' es el formato BIG ENDIAN
    # def encode(self):
    #     header = struct.pack("!BBBII", self.message_type, 
    #                         self.transfer_type,
    #                         self.protocol_type,
    #                         self.packet_number,
    #                         self.ack_number)
    #     return header + self.payload
    
    # @staticmethod
    # def decode(data):
    #     header_data = data[:HEADER_SIZE]
    #     payload = data[HEADER_SIZE:]
    #     message_type, transfer_type, protocol_type, packet_number, \
    #         ack_number = struct.unpack("!BBBII", header_data)
    #     return Message(message_type, transfer_type, protocol_type, packet_number, ack_number, payload)
    


    # def get_payload(self):
    #     return self.payload

class Decoder:
    @staticmethod
    def decode_fixed_header(data):
        message_type = struct.unpack("!B", data)
        return message_type[0]

    @staticmethod
    def size_without_fixed_header(message_type):
        if message_type == Message.INITIATE:
            return Initiate.MESSAGE_SIZE - Message.FIXED_HEADER_SIZE
        elif message_type == Message.INACK:
            return Inack.MESSAGE_SIZE - Message.FIXED_HEADER_SIZE
        elif message_type == Message.SEND:
            return Send.MESSAGE_SIZE - Message.FIXED_HEADER_SIZE
        elif message_type == Message.SENACK:
            return Senack.MESSAGE_SIZE - Message.FIXED_HEADER_SIZE

    @staticmethod
    def decode_after_fixed_header(message_type, data):
        if message_type == Message.INITIATE:
            return Initiate.decode_after_fixed_header(data)
        elif message_type == Message.INACK:
            return Inack.decode_after_fixed_header(data)
        elif message_type == Message.SEND:
            return Send.decode_after_fixed_header(data)
        elif message_type == Message.SENACK:
            return Senack.decode_after_fixed_header(data)
        elif message_type == Message.ESTABLISHED:
            return Established.decode_after_fixed_header(data)
        else:
            raise ValueError("Invalid message type")

class Initiate(Message):
    MESSAGE_SIZE = 3 # message_type + transfer_type + protocol_type

    def __init__(self, transfer_type, protocol_type):
        self.message_type = Message.INITIATE
        self.transfer_type = transfer_type
        self.protocol_type = protocol_type
        return
    
    def encode(self):
        return struct.pack("!BBB", self.message_type, self.transfer_type, self.protocol_type)

    @staticmethod
    def decode_after_fixed_header(data):
        transfer_type, protocol_type = struct.unpack("!BB", data)
        return Initiate(transfer_type, protocol_type)

class Inack(Message):
    MESSAGE_SIZE = 3 # message_type + transfer_type + protocol_type

    def __init__(self, transfer_type, protocol_type):
        self.message_type = Message.INACK
        self.transfer_type = transfer_type
        self.protocol_type = protocol_type
        return

    def encode(self):
        return struct.pack("!BBB", self.message_type, self.transfer_type, self.protocol_type)

    @staticmethod
    def decode_after_fixed_header(data):
        transfer_type, protocol_type = struct.unpack("!BB", data)
        return Inack(transfer_type, protocol_type)

class Established(Message):
    MESSAGE_SIZE = 1 # message_type

    def __init__(self):
        self.message_type = Message.ESTABLISHED
        return

    def encode(self):
        return struct.pack("!B", self.message_type)

    @staticmethod
    def decode_after_fixed_header(data):
        return Established()

class Send(Message):
    VARIABLE_HEADER_SIZE = 4 # sequence_number
    PAYLOAD_SIZE = 1000
    MESSAGE_SIZE = Message.FIXED_HEADER_SIZE + VARIABLE_HEADER_SIZE + PAYLOAD_SIZE # message_type + sequence_number + payload

    def __init__(self, sequence_number, payload):
        self.message_type = Message.SEND
        self.sequence_number = sequence_number
        self.payload = payload
        return
    
    def encode(self):
        return struct.pack("!BI", self.message_type, self.sequence_number) + self.payload

    @staticmethod
    def decode_after_fixed_header(data):

        variable_header_data = data[:Send.VARIABLE_HEADER_SIZE]

        sequence_number = struct.unpack("!I", variable_header_data)[0]
        payload = data[Send.VARIABLE_HEADER_SIZE:]
        return Send(sequence_number, payload)

class Senack(Message):
    MESSAGE_SIZE = 5 # message_type + ack_number

    def __init__(self, ack_number):
        self.message_type = Message.SENACK
        self.ack_number = ack_number
        return
    
    def encode(self):
        return struct.pack("!BI", self.message_type, self.ack_number)

    @staticmethod
    def decode_after_fixed_header(data):
        ack_number = struct.unpack("!I", data)[0]
        return Senack(ack_number)
    