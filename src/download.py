from lib.args_parser import parse_download_arguments
from lib.client import Client
from lib.constants import *
from lib.log import prepare_logging

if __name__ == "__main__":
    args = parse_download_arguments()
    prepare_logging(args)
    client = Client(args.host, args.port, args)
    client.start()
    #client.download()
    