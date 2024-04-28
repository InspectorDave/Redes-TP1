import ctypes
from lib.constants import *

# El header (compuesto por packet_number y ack_number) debe ser
# menor que el HEADER_SIZE
class Mesagge:
    def __init__(self, packet_number, ack_number):
        self.packet_number = ctypes.c_uint32(packet_number) # 4Bytes
        self.ack_number = ctypes.c_uint32(packet_number) # 4Bytes
        self.payload = b''
        return
    
    def calc_payload():
        return (BUFFER_SIZE - HEADER_SIZE) // 8