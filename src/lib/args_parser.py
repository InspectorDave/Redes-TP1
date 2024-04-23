import argparse

def parse_server_arguments():
    parser = argparse.ArgumentParser(prog='start-server.py', description='<command description>')

    parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    parser.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')
    parser.add_argument('-H', '--host', action='store', type=str, help='service IP address')
    parser.add_argument('-p', '--port', action='store', type=int, help='service port')
    parser.add_argument('-s', '--storage', action='store', type=str, help='storage dir path')
    
    args = parser.parse_args()
    
    if args.verbose:
        print("Verbose mode enabled")
    elif args.quiet:
        print("Quiet mode enabled")
    if args.host:
        print("Host:", args.host)    
    if args.port:
        print("Port:", args.port)
    if args.storage:
        print("Storage directory:", args.storage)
    return args

def parse_upload_arguments():
    return

def parse_download_arguments():
    return
