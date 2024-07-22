from src.utils.model_management import ModelManager

def deploy_model(config, model_filename):
    model_manager = ModelManager(config['models']['path'])
    
    # First, promote to staging
    model_manager.promote_to_staging(model_filename)
    print(f"Model {model_filename} promoted to staging.")
    
    # Then, promote to production
    model_manager.promote_to_production(model_filename)
    print(f"Model {model_filename} promoted to production.")