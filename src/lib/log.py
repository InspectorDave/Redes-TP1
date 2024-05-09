import logging

RED = "\033[91m"
WHITE = "\033[0m"
GREEN = "\033[92m"
BLUE = "\033[94m"

error_format = logging.Formatter(f"{RED}[%(levelname)s]{WHITE}- %(message)s")
info_format = logging.Formatter(f"{GREEN}[%(levelname)s]{WHITE}- %(message)s")
debug_format = logging.Formatter(f"{BLUE}[%(levelname)s]{WHITE}- %(message)s")

class OwnFormatter(logging.Formatter):

    def format(self, record):
        if record.levelno == logging.INFO:
            return info_format.format(record)
        elif record.levelno == logging.DEBUG:
            return debug_format.format(record)
        else:
            return error_format.format(record)


stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(OwnFormatter())

def prepare_logging(args):
    def level_verbosity():
        if args.verbose:
            return logging.DEBUG
        elif args.quiet:
            return logging.ERROR
        else:
            return logging.INFO

    logging.basicConfig(level=level_verbosity(), handlers=[stdout_handler])
