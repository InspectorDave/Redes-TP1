from lib.protocols.protocol import Protocol
from lib.protocols.stop_and_wait import StopAndWaitProtocol
from lib.protocols.go_back_n import GoBackNProtocol

class ProtocolFactory:
    @staticmethod
    def create(protocol_name):
        match protocol_name:
            case Protocol.STOP_AND_WAIT:
                session_protocol = StopAndWaitProtocol()
            case Protocol.GO_BACK_N:
                session_protocol = GoBackNProtocol()

        return session_protocol
