import pandas as pd
import yaml
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from src.utils.experiment_tracking import ExperimentTracker
from src.utils.model_management import ModelManager
from src.evaluation.evaluate_model import evaluate_model
from src.visualization.visualize import generate_model_report

def train_model(X, y, config):
    tracker = ExperimentTracker(config['logs']['path'])
    model_manager = ModelManager(config['models']['path'])
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=config['train']['test_size'], 
        random_state=config['train']['random_state']
    )
    
    tracker.start_experiment()
    
    model = RandomForestClassifier(**config['model']['params'])
    model.fit(X_train, y_train)
    
    metrics = evaluate_model(model, X_test, y_test)
    
    for param, value in config['model']['params'].items():
        tracker.log_param(param, value)
    
    for metric, value in metrics.items():
        tracker.log_metric(metric, value)
    
    tracker.end_experiment()
    
    model_path = model_manager.save_experiment_model(model, metrics)
    print(f"Model saved at: {model_path}")
    
    # Generate model report
    generate_model_report(model, X_test, y_test, X.columns, config)
    
    return model, metrics, model_path

if __name__ == '__main__':
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
    
    from src.data.make_dataset import load_data
    X, y = load_data(config)
    train_model(X, y, config)