from src.utils.all_utils import create_directory, read_yaml, copy_file
import argparse
import os
from pprint import pprint
import logging
from tqdm import tqdm

logging_str = "[%(asctime)s:  %(levelname)s: %(module)s]:  %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename = os.path.join(log_dir, "running_logs.log"),
                                            level = logging.INFO,
                                            format = logging_str, 
                                            filemode = 'a')   
                         
        
def get_data(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    
        

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
     
    