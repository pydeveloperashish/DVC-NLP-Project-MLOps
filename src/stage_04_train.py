from src.utils.all_utils import create_directory, read_yaml, copy_file
from src.utils.models import load_full_model, get_unique_path_to_save_model
from src.utils.callbacks import get_callbacks
import argparse
import os
from pprint import pprint
import logging
from src.utils.data_management import train_valid_generator

logging_str = "[%(asctime)s:  %(levelname)s: %(module)s]:  %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename = os.path.join(log_dir, "running_logs.log"),
                                            level = logging.INFO,
                                            format = logging_str, 
                                            filemode = 'a')   
                  
  
def train_model(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    
    artifacts = config['artifacts']
    artifacts_dir = artifacts['Artifacts_dir']
    
    train_model_dir_path = os.path.join(artifacts_dir, artifacts['Trained_Model_Dir'])
    create_directory([train_model_dir_path])
    
    untrained_full_model_path = os.path.join(artifacts_dir,
                artifacts['Base_model_dir'], artifacts['Updated_Base_model_name'])       
                
    model = load_full_model(untrained_full_model_path)
    
    callback_dir_path = os.path.join(artifacts_dir, artifacts['Callbacks_dir'])
    callbacks = get_callbacks(callback_dir_path)                                         
    
    train_generator, valid_generator = train_valid_generator(
        data_dir = artifacts["Data_dir"],
        IMAGE_SIZE = tuple(params["IMAGE_SIZE"][:-1]),
        BATCH_SIZE = params["BATCH_SIZE"],
        do_data_augmentation = params["AUGMENTATION"]
    )
    
    
    steps_per_epoch = train_generator.samples // train_generator.batch_size
    validation_steps = valid_generator.samples // valid_generator.batch_size
    
    model.fit(
        train_generator,
        validation_data = valid_generator,
        epochs = params["EPOCHS"],
        steps_per_epoch = steps_per_epoch,
        validation_steps = validation_steps,
        callbacks = callbacks
    )
    
    logging.info("Training Completed !!!!!")
    
    trained_model_dir = os.path.join(artifacts_dir, artifacts['Trained_Model_Dir'])
    create_directory([trained_model_dir])
    
    model_file_path = get_unique_path_to_save_model(trained_model_dir)
    model.save(model_file_path)
    
    logging.info(f"Trained model is saved  at: {model_file_path}")
                                     
                        
if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default = "config/config.yaml")
    args.add_argument("--params", "-p", default = "params.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> Stage four started")
        train_model(config_path = parsed_args.config, 
                           params_path = parsed_args.params)
        
        logging.info("Stage four completed: training completed and model is saved >>>>>\n\n")
    except Exception as e:
        logging.exception(e)
        raise e
     