from lib.args_parser import parse_download_arguments
from lib.client import Client

if __name__ == "__main__":
    args = parse_download_arguments()
    client = Client(args.host, args.port, args)
    client.start()
