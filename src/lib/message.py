from lib.constants import *
import struct

# El header (compuesto por packet_number y ack_number) debe ser
# menor que el HEADER_SIZE

# IMPORTANTE: Al agregar un campo al header 
# hay que modificar la funcion encode() y decode() y HEADER_SIZE
class Message:
    def __init__(self, packet_number, ack_number, offset, payload):
        self.packet_number = packet_number
        self.ack_number = ack_number
        self.offset = offset
        self.payload = payload
        return
    
    # El primer parametro de struct.pack es el formato. Cada I representa
    # un unsigned int de 32 bits, es decir, 4 Bytes y '!' es el formato
    # BIG ENDIAN
    def encode(self):
        header = struct.pack("!III", self.packet_number, self.ack_number, self.offset)
        #padding_length = HEADER_SIZE - len(header)
        #if padding_length > 0:
        #    padding = b'\x00' * padding_length
        #    header += padding
        return header + self.payload
    
    
    def decode(self, data):
        header_data = data[:HEADER_SIZE]
        payload = data[HEADER_SIZE:]
        packet_number, ack_number, offset = struct.unpack("!III", header_data)
        return Message(packet_number, ack_number, offset, payload)