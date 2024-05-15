import argparse
import lib.constants as CONST
import os


def parse_server_arguments():
    parser = argparse.ArgumentParser(prog='start-server.py',
                                     description='<command description>')
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
                        '--host',  # Nombre de la variable
                        metavar='ADDR',  # Cómo se muestra al hacer -h
                        default=CONST.DEFAULT_HOST,
                        action='store',
                        type=str,
                        help='service IP address')

    parser.add_argument('-p',
                        '--port',
                        default=CONST.DEFAULT_PORT,
                        action='store',
                        type=int,
                        help='service port')

    parser.add_argument('-s',
                        '--storage',
                        metavar='DIRPATH',
                        default=CONST.DEFAULT_SERVER_STORAGE,
                        action='store',
                        type=str,
                        help='storage dir path')

    args = parser.parse_args()
    _verify_server_arguments(args)
    return args


def _verify_server_arguments(args):
    if not os.path.exists(args.storage):
        os.mkdir(args.storage)
    return


def parse_upload_arguments():
    parser = argparse.ArgumentParser(prog='upload.py',
                                     description='<command description>')
    _add_common_args(parser)

    parser.add_argument('-s',
                        '--src',
                        action='store',
                        default=CONST.DEFAULT_UPLOAD_FILE_PATH,
                        type=str,
                        help='source file path')

    parser.add_argument('-n',
                        '--name',
                        default=CONST.DEFAULT_UPLOAD_FILE_NAME,
                        action='store',
                        type=str,
                        help='file name')

    parser.add_argument('-r',
                        '--protocol',
                        action='store',
                        type=str,
                        help='protocol to use: s=StopAndWait or g=GoBackN',
                        required=True)

    args = parser.parse_args()
    _verify_upload_arguments(args)
    return args


def _verify_upload_arguments(args):
    full_name = os.path.join(args.src, args.name)
    if not os.path.exists(full_name):
        raise FileNotFoundError(f"Directory '{full_name}' does not exist.")
    if args.protocol != 's' and args.protocol != 'g':
        raise Exception(
            "Incorrect protocol. Use 's' or 'g'")
    return


def parse_download_arguments():
    parser = argparse.ArgumentParser(prog='download.py',
                                     description='<command description>')
    _add_common_args(parser)

    parser.add_argument('-d',
                        '--dst',
                        default=CONST.DEFAULT_DOWNLOAD_DST,
                        metavar='FILEPATH',
                        action='store',
                        type=str,
                        help='destination file path')

    parser.add_argument('-n',
                        '--name',
                        default=CONST.DEFAULT_DOWNLOAD_FILE_NAME,
                        metavar='FILENAME',
                        action='store',
                        type=str,
                        help='file name')

    parser.add_argument('-r',
                        '--protocol',
                        action='store',
                        type=str,
                        help='protocol to use: s= StopAndWait; g=GoBackN',
                        required=True)

    args = parser.parse_args()
    _verify_download_arguments(args)
    return args


def _verify_download_arguments(args):
    if not os.path.exists(args.dst):
        os.mkdir(args.dst)
    if args.protocol != 's' and args.protocol != 'g':
        raise Exception(
            "Incorrect protocol. Use 's' or 'g'")
    return


def _add_common_args(parser: argparse.ArgumentParser):
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
                        default=CONST.DEFAULT_HOST,
                        action='store',
                        type=str,
                        help='server IP address')

    parser.add_argument('-p',
                        '--port',
                        default=CONST.DEFAULT_PORT,
                        action='store',
                        type=int,
                        help='server port')
    return
