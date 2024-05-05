import argparse
from lib.constants import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_SERVER_STORAGE

def parse_server_arguments():
    parser = argparse.ArgumentParser(prog='start-server.py', description='<command description>')
    group_verbosity = parser.add_mutually_exclusive_group(required=False)
    
    group_verbosity.add_argument('-v',
                                '--verbose',
                                action='store_true',
                                help='increase output verbosity')
    
    group_verbosity.add_argument('-q',
                                '--quiet',
                                action='store_true',
                                help='decrease output verbosity')
    
    parser.add_argument('-H',
                        '--host', # Nombre de la variable
                        metavar = 'ADDR', # Cómo se muestra al hacer -h
                        default = DEFAULT_HOST,
                        action='store',
                        type=str,
                        help='service IP address')
    
    parser.add_argument('-p',
                        '--port',
                        default = DEFAULT_PORT,
                        action='store',
                        type=int,
                        help='service port')
    
    parser.add_argument('-s',
                        '--storage',
                        metavar = 'DIRPATH',
                        default = DEFAULT_SERVER_STORAGE,
                        action='store',
                        type=str,
                        help='storage dir path')
    
    args = parser.parse_args()
    if args.verbose:
        print(args)
    return args


def parse_upload_arguments():
    parser = argparse.ArgumentParser(prog='upload.py', description='<command description>')
    _add_common_args(parser)
    
    parser.add_argument('-s',
                        '--src',
                        action='store',
                        type=str,
                        help='source file path')
    
    parser.add_argument('-n',
                        '--name',
                        action='store',
                        type=str,
                        help='file name')
    
    parser.add_argument('-r',
                        '--protocol',
                        action='store',
                        type = str,
                        help='protocol to use: s= StopAndWait; g=GoBackN',
                        default='s')
    
    args = parser.parse_args()
    if args.verbose:
        print(args)
    return args


def parse_download_arguments():
    parser = argparse.ArgumentParser(prog='download.py', description='<command description>')
    _add_common_args(parser)
    
    parser.add_argument('-d',
                        '--dst',
                        metavar = 'FILEPATH',
                        action='store',
                        type=str,
                        help='destination file path')
    
    parser.add_argument('-n',
                        '--name',
                        metavar= 'FILENAME',
                        action='store',
                        type=str,
                        help='file name')
    
    parser.add_argument('-r',
                        '--protocol',
                        action='store',
                        type = str,
                        help='protocol to use: s= StopAndWait; g=GoBackN',
                        default='s')
    
    args = parser.parse_args()
    if args.verbose:
        print(args)
    return args




def _add_common_args(parser:argparse.ArgumentParser):
    group_verbosity = parser.add_mutually_exclusive_group(required=False)
    
    group_verbosity.add_argument('-v',
                                '--verbose',
                                action='store_true',
                                help='increase output verbosity')
    
    group_verbosity.add_argument('-q',
                                '--quiet',
                                action='store_true',
                                help='decrease output verbosity')    
    
    parser.add_argument('-H',
                        '--host',
                        default=DEFAULT_HOST,
                        action='store',
                        type=str,
                        help='server IP address')
    
    parser.add_argument('-p',
                        '--port',
                        default=DEFAULT_PORT,
                        action='store',
                        type=int,
                        help='server port')
    return
