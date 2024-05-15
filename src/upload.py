from lib.args_parser import parse_upload_arguments
from lib.client import Client
from lib.connection import Connection
from lib.constants import *
from lib.file_manager import *
from lib.log import prepare_logging
from lib.protocols.protocol import Protocol
from lib.protocols.protocol_factory import ProtocolFactory

if __name__ == "__main__":
    try:
        args = parse_upload_arguments()
    except Exception as e:
        logging.error(e)
        exit(-1)
    prepare_logging(args)
    protocol = ProtocolFactory.create_from_arguments(args.protocol)
    connection = Connection((args.host, args.port), Protocol.UPLOAD, protocol, args.name)
    client = Client(connection, args.src)
    client.start()
    client.upload()
