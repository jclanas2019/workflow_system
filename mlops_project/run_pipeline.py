import yaml
import os
from src.models.train_model import train_model
from src.evaluation.evaluate_model import compare_models
from src.deployment.deploy_model import deploy_model
from src.utils.model_management import ModelManager
from src.data.make_dataset import load_data

def run_pipeline():
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
    
    # Load and preprocess data
    X, y = load_data(config)
    
    # Train new model
    new_model, new_metrics, model_path = train_model(X, y, config)
    
    # Get current production model
    model_manager = ModelManager(config['models']['path'])
    try:
        current_model = model_manager.get_production_model()
        
        # Compare new model with current production model
        _, _, improvement = compare_models(current_model, new_model, X, y)
        
        # Define a threshold for model improvement
        if improvement['f1'] > 0.02:  # If F1 score improves by more than 2%
            deploy_model(config, os.path.basename(model_path))
        else:
            print("New model does not show significant improvement. Not deploying.")
    except ValueError:
        # No production model exists, deploy the new model
        deploy_model(config, os.path.basename(model_path))

if __name__ == '__main__':
    run_pipeline()