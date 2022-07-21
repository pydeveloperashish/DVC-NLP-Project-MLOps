from src.utils.all_utils import create_directory, read_yaml, copy_file
import argparse
import os
from pprint import pprint
import logging
from tqdm import tqdm
import random


logging_str = "[%(asctime)s:  %(levelname)s: %(module)s]:  %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename = os.path.join(log_dir, "running_logs.log"),
                                            level = logging.INFO,
                                            format = logging_str, 
                                            filemode = 'a')   
                         
        
def get_data(config_path, params_path):
    ## converting xml data to tsv
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    
    source_data = config["source_data_dirs"]
    input_data = os.path.join(source_data['data_dir'], source_data['data_file'])
    
    split = params['prepare']['split']
    seed = params['prepare']['seed']
    
    random.seed(seed)
    
    artifacts = config['artifacts']
    
    prepared_data_dir_path = os.path.join(artifacts['Artifacts_dir'], artifacts['Prepared_Data_dir'])
    create_directory([prepared_data_dir_path])
    
    train_data_path = os.path.join(prepared_data_dir_path, artifacts['Trained_Data'])
    test_data_path = os.path.join(prepared_data_dir_path, artifacts['Test_Data'])
        
    with open(input_data, encoding='utf8') as fd_in:
        with open(train_data_path, "w", encoding='utf8') as fd_out_train:
            with open(test_data_path, "w", encoding='utf8') as fd_out_test:
                #processed_posts(fd_in, fd_out_train, fd_out_test, "<python>", split)
                pass

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default = "config/config.yaml")
    args.add_argument("--params", "-p", default = "params.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> Stage one started")
        get_data(config_path = parsed_args.config, params_path = parsed_args.params)
        logging.info("Stage one completed!!! >>>>>\n")
    except Exception as e:
        logging.exception(e)
        raise e
     
    