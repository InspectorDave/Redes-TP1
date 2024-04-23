from lib.args_parser import parse_server_arguments
from lib.server import Server

if __name__ == "__main__":
    args = parse_server_arguments()
    server = Server(args.host, args.port, args)
    server.start()