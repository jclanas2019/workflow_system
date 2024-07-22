import asyncio
import ssl
import os
from .cert_generator import generate_certificates
from etl.etl_processor import ETLProcessor
import pyfiglet

class SecureDataClient:
    def __init__(self, host: str, port: int, cert_dir: str):
        self.host = host
        self.port = port
        self.cert_dir = cert_dir
        generate_certificates(cert_dir)
        self.data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'source_data.csv'))
        self.print_ascii_message()
        # Inicializa el archivo de datos
        with open(self.data_file, 'w') as f:
            f.write('existing_column\n')

    def print_ascii_message(self):
        ascii_banner = pyfiglet.figlet_format("Secure Data Client")
        print(ascii_banner)

    async def process_data(self, data: str):
        print(f"Procesando datos: {data}")
        with open(self.data_file, 'a') as f:
            f.write(f"{data.split(',')[1]}\n")

    async def read_data(self, reader):
        while True:
            data = await reader.readline()
            if not data:
                break
            await self.process_data(data.decode('utf-8').strip())

    async def connect(self):
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=os.path.join(self.cert_dir, 'server.crt'))
        # Permitir certificados autofirmados
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        reader, writer = await asyncio.open_connection(self.host, self.port, ssl=ssl_context)
        await self.read_data(reader)

    def run_etl(self):
        etl_processor = ETLProcessor(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'etl', 'config.yaml')))
        etl_processor.run()

if __name__ == "__main__":
    data_client = SecureDataClient('localhost', 9999, 'certs')
    asyncio.run(data_client.connect())
    data_client.run_etl()
