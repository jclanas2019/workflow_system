import sys
import os
import asyncio
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

# Añadir el directorio raíz al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from streaming.secure_client import SecureDataClient

def main():
    data_client = SecureDataClient('localhost', 9999, 'certs')
    asyncio.run(data_client.connect())

if __name__ == "__main__":
    main()
