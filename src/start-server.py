from lib.args_parser import parse_server_arguments
from lib.server import Server
from lib.constants import *

if __name__ == "__main__":
    args = parse_server_arguments()
    server = Server(args.host, args.port, args)
    server.start()

# El server debería tener un socket que escucha conexiones y una vez
# conectado un cliente, asignarle un nuevo socket para la comunicacion
