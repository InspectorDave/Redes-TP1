import ctypes

class Mesagge:
    def __init__(self, packet_number, ack_number):
        self.packet_number = ctypes.c_uint32(packet_number)
        self.ack_number = ctypes.c_uint32(packet_number)
        self.payload = b''
        return