import pandas as pd
import numpy as np
import yaml
import os

class ETLProcessor:
    def __init__(self, config_path: str):
        # Calcular la ruta absoluta del archivo de configuración
        config_path = os.path.abspath(config_path)
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.input_path = os.path.abspath(os.path.join(os.path.dirname(config_path), '..', config['input_path']))
        self.output_path = os.path.abspath(os.path.join(os.path.dirname(config_path), '..', config['output_path']))
        self.threshold_value = config['threshold_value']
        self.data = None

    def extract(self):
        self.data = pd.read_csv(self.input_path)

    def transform(self):
        self.data = self.data.dropna()
        self.data['new_column'] = self.data['existing_column'] * np.random.rand(len(self.data))
        self.data = self.data[self.data['new_column'] > self.threshold_value]

    def load(self):
        self.data.to_csv(self.output_path, index=False)

    def run(self):
        self.extract()
        self.transform()
        self.load()
