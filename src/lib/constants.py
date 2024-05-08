import ctypes

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9000
DEFAULT_SERVER_STORAGE = '../server_storage/'
DEFAULT_FILE_NAME = 'file1.txt'

DEFAULT_UPLOAD_FILE_PATH = '../test_files/'
DEFAULT_UPLOAD_FILE_NAME = 'test_file_2.txt'

DEFAULT_DOWNLOAD_DST = '../downloads/'
DEFAULT_DOWNLOAD_FILE_NAME = 'file1.txt'

BUFFER_SIZE = 1024 # Tamanio del mensaje (Debe ser mayor que el header)
HEADER_SIZE = 11 # Modificar si se agregan campos al header en clase Message
PAYLOAD_SIZE = (BUFFER_SIZE-HEADER_SIZE) # Tamanio de los datos

RECV_BUFFER_SIZE = 8192

UPLOAD = 0
DOWNLOAD = 1

STOP_AND_WAIT = 's'
GO_BACK_N = 'g'

STOP_AND_WAIT_N = 0
GO_BACK_N_N = 1

FILE_MODE_WRITE = 'w'
FILE_MODE_READ = 'r'

TIME_OUT = 1
KEEP_ALIVE = 4
