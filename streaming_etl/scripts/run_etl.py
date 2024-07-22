import sys
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

# Añadir el directorio raíz al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from etl.etl_processor import ETLProcessor

def main():
    # Calcular la ruta correcta para config.yaml
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../etl/config.yaml'))
    etl_processor = ETLProcessor(config_path)
    etl_processor.run()

if __name__ == "__main__":
    main()
