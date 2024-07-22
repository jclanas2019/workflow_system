import json
import os
from datetime import datetime

class ExperimentTracker:
    def __init__(self, log_path):
        self.log_path = log_path
        self.current_experiment = None

    def start_experiment(self):
        self.current_experiment = {
            'timestamp': datetime.now().isoformat(),
            'params': {},
            'metrics': {}
        }

    def log_param(self, key, value):
        if self.current_experiment is None:
            raise ValueError("No experiment in progress. Call start_experiment() first.")
        self.current_experiment['params'][key] = value

    def log_metric(self, key, value):
        if self.current_experiment is None:
            raise ValueError("No experiment in progress. Call start_experiment() first.")
        self.current_experiment['metrics'][key] = value

    def end_experiment(self):
        if self.current_experiment is None:
            raise ValueError("No experiment in progress.")
        
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(self.current_experiment)
        
        with open(self.log_path, 'w') as f:
            json.dump(logs, f, indent=2)
        
        self.current_experiment = None