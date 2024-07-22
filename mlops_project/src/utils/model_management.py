import os
import joblib
from datetime import datetime

class ModelManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.experiments_dir = os.path.join(base_dir, 'experiments')
        self.staging_dir = os.path.join(base_dir, 'staging')
        self.production_dir = os.path.join(base_dir, 'production')
        
        for dir in [self.experiments_dir, self.staging_dir, self.production_dir]:
            os.makedirs(dir, exist_ok=True)

    def save_experiment_model(self, model, metrics):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = os.path.join(self.experiments_dir, f"model_{timestamp}.joblib")
        metadata_path = os.path.join(self.experiments_dir, f"metadata_{timestamp}.joblib")
        
        joblib.dump(model, model_path)
        joblib.dump(metrics, metadata_path)
        
        return model_path

    def promote_to_staging(self, model_filename):
        src_path = os.path.join(self.experiments_dir, model_filename)
        dst_path = os.path.join(self.staging_dir, model_filename)
        os.rename(src_path, dst_path)
        
        src_metadata = src_path.replace('model_', 'metadata_')
        dst_metadata = dst_path.replace('model_', 'metadata_')
        os.rename(src_metadata, dst_metadata)

    def promote_to_production(self, model_filename):
        src_path = os.path.join(self.staging_dir, model_filename)
        dst_path = os.path.join(self.production_dir, model_filename)
        os.rename(src_path, dst_path)
        
        src_metadata = src_path.replace('model_', 'metadata_')
        dst_metadata = dst_path.replace('model_', 'metadata_')
        os.rename(src_metadata, dst_metadata)

    def get_production_model(self):
        model_files = [f for f in os.listdir(self.production_dir) if f.startswith("model_")]
        if not model_files:
            raise ValueError("No production model found.")
        
        latest_model = max(model_files)
        model_path = os.path.join(self.production_dir, latest_model)
        
        return joblib.load(model_path)

    def get_model_metrics(self, model_filename, stage='experiments'):
        if stage == 'experiments':
            dir_path = self.experiments_dir
        elif stage == 'staging':
            dir_path = self.staging_dir
        elif stage == 'production':
            dir_path = self.production_dir
        else:
            raise ValueError("Invalid stage. Choose from 'experiments', 'staging', or 'production'.")
        
        metadata_filename = f"metadata_{model_filename[6:]}"
        metadata_path = os.path.join(dir_path, metadata_filename)
        
        return joblib.load(metadata_path)