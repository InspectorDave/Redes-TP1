import argparse

def parse_server_arguments():
    parser = argparse.ArgumentParser(prog='start-server.py', description='<command description>')

    group_verbosity = parser.add_mutually_exclusive_group(required=False)
    group_verbosity.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    group_verbosity.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')
    
    parser.add_argument('-H', '--host', action='store', type=str, help='service IP address')
    parser.add_argument('-p', '--port', action='store', type=int, help='service port')
    parser.add_argument('-s', '--storage', action='store', type=str, help='storage dir path')
    
    args = parser.parse_args()
    
    if args.verbose:
        print(args)

    return args

def parse_upload_arguments():
    parser = argparse.ArgumentParser(prog='upload.py', description='<command description>')
    _add_common_args(parser)
    parser.add_argument('-s', '--src', action='store', type=str, help='source file path')
    parser.add_argument('-n', '--name', action='store', type=str, help='file name')
    args = parser.parse_args()

    if args.verbose:
        print(args)
    return args

def parse_download_arguments():
    parser = argparse.ArgumentParser(prog='download.py', description='<command description>')
    _add_common_args(parser)

    parser.add_argument('-d', '--dst', action='store', type=str, help='destination file path')
    parser.add_argument('-n', '--name', action='store', type=str, help='file name')

    args = parser.parse_args()

    if args.verbose:
        print(args)
    return args


def _add_common_args(parser):
    group_verbosity = parser.add_mutually_exclusive_group(required=False)
    group_verbosity.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    group_verbosity.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')
    
    parser.add_argument('-H', '--host', action='store', type=str, help='service IP address')
    parser.add_argument('-p', '--port', action='store', type=int, help='service port')
    return
