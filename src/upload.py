from lib.args_parser import parse_upload_arguments
from lib.client import Client
from lib.constants import *
from lib.file_manager import *
import logging
from lib.log import prepare_logging
from lib.protocols.protocol import Protocol
from lib.protocols.protocol_factory import ProtocolFactory

if __name__ == "__main__":
    args = parse_upload_arguments()
    prepare_logging(args)
    protocol = ProtocolFactory.create_from_arguments(args.protocol)
    client = Client((args.host, args.port), Protocol.UPLOAD, protocol)
    client.start()
    client.upload(args.src, args.name)
    