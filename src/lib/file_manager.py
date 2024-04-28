class FileManager:
    def __init__(self):
        return
    
    # Deberia ir leyendo por partes, en vez de guardarlo todo en una variable?
    def read_file_bytes(self, filepath):
        try:
            # Con 'with' el archivo se cierra automaticamente
            with open(filepath, 'rb') as f: 
                return f.read()
        except FileNotFoundError:
            print(f"Error: El archivo '{filepath}' no fue encontrado.")
        except Exception as e:
            print(f"Error desconocido al leer el archivo: {e}")
        return
    
    def write_file_bytes(self, filepath, data):
        try:
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"Se ha escrito correctamente el archivo '{filepath}'.")
        except FileNotFoundError:
            print(f"Error: La ruta '{filepath}' no fue encontrada.")
        except PermissionError:
            print(f"Error: No tienes permisos para escribir en la ruta '{filepath}'.")
        except Exception as e:
            print(f"Error desconocido al escribir el archivo: {e}")

