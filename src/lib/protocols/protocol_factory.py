from lib.protocols.stop_and_wait import StopAndWaitProtocol
from lib.protocols.go_back_n import GoBackNProtocol
from lib.protocols.protocol import Protocol

class ProtocolFactory:
    @staticmethod
    def create(protocol_name):
        if (protocol_name == Protocol.STOP_AND_WAIT):
                session_protocol = StopAndWaitProtocol()
        elif (protocol_name == Protocol.GO_BACK_N):
                session_protocol = GoBackNProtocol()

        return session_protocol

    def create_from_arguments(protocol_name):
        if (protocol_name == 's'):
                session_protocol = StopAndWaitProtocol()
        elif (protocol_name == 'g'):
                session_protocol = GoBackNProtocol()

        return session_protocol