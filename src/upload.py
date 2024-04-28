from lib.args_parser import parse_download_arguments
from lib.client import Client
from lib.constants import *
from lib.file_manager import *

if __name__ == "__main__":
    args = parse_download_arguments()
    #file_manager = FileManager()
    #file_content = file_manager.read_file_bytes("./lib/test_file_3.txt")
    #print(file_content)
    if (args.host and args.port):
        client = Client(args.host, args.port, args)
        client.start()
        client.upload("./lib/test_file_1.txt")
    else:
        client = Client(DEFAULT_HOST, DEFAULT_PORT, args)
        client.start()
        client.upload("./lib/test_file_1.txt")