from lib.constants import FILE_MODE_READ, FILE_MODE_WRITE
import os

class FileManager:
    def __init__(self, mode, filepath, filename):
        self.file = None
        self.file_number = 1
        if not mode or not filepath:
            raise ValueError("Error en la creación del file manager")
        
        if mode == FILE_MODE_READ:
            self.open_to_read(filepath, filename)
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"El directorio '{filepath}' no existe.")
        
        elif mode == FILE_MODE_WRITE:
            if not os.path.exists(filepath):
                os.makedirs(filepath)
                print(f"Directorio '{filepath}' creado exitosamente.")
            else:
                print(f"Se utilizará el directorio existente: '{filepath}'.")
            self.open_to_write(filepath, filename)
        
        else:
            raise ValueError("Error en el modo de creación del file manager")


    def open_to_read(self, filepath, filename):
        try:
            self.file = open(os.path.join(filepath, filename), 'rb')
        except FileNotFoundError:
            print(f"Error: El archivo '{filename}' no fue encontrado.")
        except Exception as e:
            print(f"Error desconocido al leer el archivo: {e}")

    # El filepath debe contener el nombre del archivo al final
    def open_to_write(self, filepath, filename):
        try:
            self.file = open(os.path.join(filepath, filename), 'wb')
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
            #print("[LOG]Chunk info: ", chunk_info)
            bytes_written = self.file.write(chunk_info)
            print("BYTES WRITTEN: ", bytes_written)
            self.file.flush()
        except Exception as e:
            print(f"Error: {e}")


    def close(self):
        if self.file:
            self.file.close()
