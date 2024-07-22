import asyncio
import ssl
import random
import datetime
import os
from .cert_generator import generate_certificates
import pyfiglet

class SecureDataServer:
    def __init__(self, host: str, port: int, cert_dir: str):
        self.host = host
        self.port = port
        self.cert_dir = cert_dir
        generate_certificates(cert_dir)
        self.print_ascii_message()

    def print_ascii_message(self):
        ascii_banner = pyfiglet.figlet_format("Secure Data Server")
        print(ascii_banner)

    async def handle_client(self, reader, writer):
        try:
            while True:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                value = random.random()
                message = f"{timestamp},{value}\n"
                writer.write(message.encode('utf-8'))
                await writer.drain()
                await asyncio.sleep(1)
        except (ConnectionResetError, asyncio.CancelledError):
            print("Cliente desconectado")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def start_server(self):
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=os.path.join(self.cert_dir, 'server.crt'), keyfile=os.path.join(self.cert_dir, 'server.key'))
        server = await asyncio.start_server(self.handle_client, self.host, self.port, ssl=ssl_context)
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    data_server = SecureDataServer('localhost', 9999, 'certs')
    asyncio.run(data_server.start_server())
