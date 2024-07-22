from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1': f1_score(y_test, y_pred, average='weighted')
    }
    
    return metrics

def compare_models(current_model, new_model, X_test, y_test):
    current_metrics = evaluate_model(current_model, X_test, y_test)
    new_metrics = evaluate_model(new_model, X_test, y_test)
    
    improvement = {}
    for metric in current_metrics:
        improvement[metric] = new_metrics[metric] - current_metrics[metric]
    
    return current_metrics, new_metrics, improvement