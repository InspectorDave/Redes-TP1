import ctypes

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9000
DEFAULT_SERVER_STORAGE = './server_storage/'
DEFAULT_DOWNLOAD_DST = './downloads/'


BUFFER_SIZE = 2048 # Tamanio del mensaje (Debe ser mayor que el header)
HEADER_SIZE = 15 # Modificar si se agregan campos al header en clase Message
PAYLOAD_SIZE = (BUFFER_SIZE-HEADER_SIZE) # Tamanio de los datos

UPLOAD: ctypes.c_int8 = 0
DOWNLOAD: ctypes.c_int8 = 1

FILE_MODE_WRITE = 'w'
FILE_MODE_READ = 'r'