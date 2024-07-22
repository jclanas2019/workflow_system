import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import os

def load_data(config):
    # For this example, we're using the iris dataset
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='target')
    
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(config['data']['raw_data_path']), exist_ok=True)
    os.makedirs(os.path.dirname(config['data']['processed_data_path']), exist_ok=True)
    
    # Save raw data
    df = pd.concat([X, y], axis=1)
    df.to_csv(config['data']['raw_data_path'], index=False)
    
    # Process data (in this case, we're not doing any processing)
    df.to_csv(config['data']['processed_data_path'], index=False)
    
    return X, y

if __name__ == '__main__':
    import yaml
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
    load_data(config)