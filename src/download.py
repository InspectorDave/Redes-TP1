from lib.args_parser import parse_download_arguments
from lib.client import Client
from lib.constants import *
from lib.file_manager import *
from lib.log import prepare_logging
from lib.protocols.protocol import Protocol
from lib.protocols.protocol_factory import ProtocolFactory

if __name__ == "__main__":
    args = parse_download_arguments()
    prepare_logging(args)
    protocol = ProtocolFactory.create_from_arguments(args.protocol)
    client = Client((args.host, args.port), Protocol.DOWNLOAD, protocol, args.name)
    client.start()
    client.download(args.dst, args.name)