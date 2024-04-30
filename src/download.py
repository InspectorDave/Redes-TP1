from lib.args_parser import parse_download_arguments
from lib.client import Client
from lib.constants import *

if __name__ == "__main__":
    args = parse_download_arguments()
    if (args.host and args.port):
        client = Client(args.host, args.port, args)
    else:
        client = Client(DEFAULT_HOST, DEFAULT_PORT, args)
    
    client.start()
    #client.download()
    