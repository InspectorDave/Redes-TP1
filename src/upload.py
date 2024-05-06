from lib.args_parser import parse_upload_arguments
from lib.client import Client
from lib.constants import *
from lib.file_manager import *
import time

if __name__ == "__main__":
    args = parse_upload_arguments()
    client = Client(args.host, args.port, args)
    client.start()
    print("[LOG] Sending file")
    print(args.src, args.name)
    client.upload(args.src, args.name)
    