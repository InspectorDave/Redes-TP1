from lib.args_parser import parse_upload_arguments
from lib.client import Client
from lib.constants import *
from lib.file_manager import *
import logging
from lib.log import prepare_logging
from lib.protocols import *

if __name__ == "__main__":
    args = parse_upload_arguments()
    prepare_logging(args)
    client = Client(args.host, args.port, UPLOAD, args)
    client.start()
    client.upload(args.src, args.name)
    