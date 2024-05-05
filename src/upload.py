from lib.args_parser import parse_download_arguments
from lib.client import Client
from lib.constants import *
from lib.file_manager import *
import time

if __name__ == "__main__":
    args = parse_download_arguments()
    client = Client(args.host, args.port, args)
    client.start()
    print("[LOG] Sending file")
    client.upload("../test_files/test_file_2.txt")
    