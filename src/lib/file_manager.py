class FileManager:
    def __init__(self, filepath):
        try:
            self.file = open(filepath, 'rb')
        except FileNotFoundError:
            print(f"Error: El archivo '{filepath}' no fue encontrado.")
        except Exception as e:
            print(f"Error desconocido al leer el archivo: {e}")
        
    def read_file_bytes(self, chunk_size):
        try:
            file_content = self.file.read(chunk_size)
            return file_content
        except Exception as e:
            print(f"Error: {e}")

    def close(self):
        self.file.close()
