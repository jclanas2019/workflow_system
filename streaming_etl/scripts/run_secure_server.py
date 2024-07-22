import sys
import os
import asyncio
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

# Añadir el directorio raíz al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from streaming.secure_server import SecureDataServer

def main():
    data_server = SecureDataServer('localhost', 9999, 'certs')
    asyncio.run(data_server.start_server())

if __name__ == "__main__":
    main()
