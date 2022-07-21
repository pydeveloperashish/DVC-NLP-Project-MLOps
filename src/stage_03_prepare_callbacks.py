from src.utils.all_utils import create_directory, read_yaml, copy_file
from src.utils.callbacks import create_and_save_checkpoint_callback, create_and_save_tensorboard_callback

import argparse
import os
from pprint import pprint
import logging

logging_str = "[%(asctime)s:  %(levelname)s: %(module)s]:  %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename = os.path.join(log_dir, "running_logs.log"),
                                            level = logging.INFO,
                                            format = logging_str, 
                                            filemode = 'a')   
                         
                        
            
def prepare_callbacks(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    
    artifacts = config['artifacts']
    artifacts_dir = artifacts['Artifacts_dir']
    
    tensorflow_log_dir = os.path.join(artifacts_dir, artifacts['Tensorboard_root_log_dir'])            
    checkpoint_dir = os.path.join(artifacts_dir, artifacts['Checkpoint_dir'])
    callbacks_dir = os.path.join(artifacts_dir, artifacts['Callbacks_dir'])
    
    create_directory(
        [tensorflow_log_dir,
        checkpoint_dir,
        callbacks_dir]
    )
    
    create_and_save_tensorboard_callback(callbacks_dir, tensorflow_log_dir)
    create_and_save_checkpoint_callback(callbacks_dir, checkpoint_dir)
    
    
if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default = "config/config.yaml")
    args.add_argument("--params", "-p", default = "params.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> Stage three started")
        prepare_callbacks(config_path = parsed_args.config, 
                           params_path = parsed_args.params)
        
        logging.info("Stage three completed: Callbacks are preared and saved as binary >>>>>")
    except Exception as e:
        logging.exception(e)
        raise e
     