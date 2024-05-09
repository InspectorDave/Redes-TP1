from lib.args_parser import parse_server_arguments
from lib.server import Server
from lib.constants import *
from lib.log import *

if __name__ == "__main__":
    try:
        args = parse_server_arguments()
    except Exception as e:
        logging.error(e)
        exit(-1)
    prepare_logging(args)
    logging.debug(f"{args}")
    server = Server(args.host, args.port, args)
    server.start()

# El server debería tener un socket que escucha conexiones y una vez
# conectado un cliente, asignarle un nuevo socket para la comunicacion
