from lib.constants import FILE_MODE_READ, FILE_MODE_WRITE
import logging

class FileManager:
    def __init__(self, mode=None, filepath=None):
        self.file = None
        if not mode or not filepath:
            logging.error(f"Error en la creación del file manager")
        if mode == FILE_MODE_READ:
            self.open_to_read(filepath)
        elif mode == FILE_MODE_WRITE:
            self.open_to_write(filepath)


    def open_to_read(self, filepath):
        try:
            self.file = open(filepath, 'rb')
        except FileNotFoundError:
            print(f"Error: El archivo '{filepath}' no fue encontrado.")
        except Exception as e:
            print(f"Error desconocido al leer el archivo: {e}")

    # El filepath debe contener el nombre del archivo al final
    def open_to_write(self, filepath):
        try:
            self.file = open(filepath, 'ab')
        except Exception as e:
            print(f"Error desconocido al abrir el archivo para escribir: {e}")
    

    def read_file_bytes(self, chunk_size):
        try:
            file_content = self.file.read(chunk_size)
            return file_content
        except Exception as e:
            print(f"Error: {e}")

    
    def write_file_bytes(self, chunk_info):
        try:
            self.file.write(chunk_info)
        except Exception as e:
            print(f"Error: {e}")


    def close(self):
        if self.file:
            self.file.close()
