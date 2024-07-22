import os
import json
from datetime import datetime
import logging
import shutil

class ExperimentManager:
    def __init__(self, base_dir="experiments"):
        self.base_dir = base_dir
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

    def create_experiment(self):
        experiment_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        experiment_dir = os.path.join(self.base_dir, experiment_id)
        os.makedirs(experiment_dir)
        os.makedirs(os.path.join(experiment_dir, "artifacts"))
        os.makedirs(os.path.join(experiment_dir, "models/test"))
        os.makedirs(os.path.join(experiment_dir, "models/production"))
        with open(os.path.join(experiment_dir, "params.json"), "w") as f:
            json.dump({}, f)
        with open(os.path.join(experiment_dir, "metrics.json"), "w") as f:
            json.dump({}, f)
        return experiment_id

    def log_params(self, experiment_id, params):
        experiment_dir = os.path.join(self.base_dir, experiment_id)
        params_file = os.path.join(experiment_dir, "params.json")
        with open(params_file, "r") as f:
            existing_params = json.load(f)
        existing_params.update(params)
        with open(params_file, "w") as f:
            json.dump(existing_params, f)

    def log_metrics(self, experiment_id, metrics):
        experiment_dir = os.path.join(self.base_dir, experiment_id)
        metrics_file = os.path.join(experiment_dir, "metrics.json")
        with open(metrics_file, "r") as f:
            existing_metrics = json.load(f)
        # Convert datetime objects to strings
        for key, value in metrics.items():
            if isinstance(value, datetime):
                metrics[key] = value.strftime("%Y-%m-%d %H:%M:%S.%f")
        existing_metrics.update(metrics)
        with open(metrics_file, "w") as f:
            json.dump(existing_metrics, f)

    def save_artifact(self, experiment_id, artifact_path):
        experiment_dir = os.path.join(self.base_dir, experiment_id)
        artifacts_dir = os.path.join(experiment_dir, "artifacts")
        os.makedirs(artifacts_dir, exist_ok=True)
        artifact_name = os.path.basename(artifact_path)
        shutil.copy2(artifact_path, os.path.join(artifacts_dir, artifact_name))

    def log_model(self, experiment_id, model_path, model_name, stage="test"):
        experiment_dir = os.path.join(self.base_dir, experiment_id)
        models_dir = os.path.join(experiment_dir, f"models/{stage}")
        os.makedirs(models_dir, exist_ok=True)
        model_destination = os.path.join(models_dir, model_name)
        shutil.copy2(model_path, model_destination)
        logging.info(f"Model {model_name} saved to {model_destination}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
