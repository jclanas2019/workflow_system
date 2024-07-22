import os

OUTPUT_DIR = 'txt'
LOG_DIR = 'log'

# Crear directorios si no existen
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
