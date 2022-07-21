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
                         
        
def get_data(config_path):
    config = read_yaml(config_path)
    source_download_dirs = config["source_download_dirs"]
    local_data_dirs = config["local_data_dirs"]
    
    for source_download_dir, local_data_dir in tqdm(zip(source_download_dirs, local_data_dirs), total = 2, desc = "List of Folders", colour = 'red'):
        create_directory(local_data_dirs)
        copy_file(source_download_dir, local_data_dir)
        

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default = "config/config.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info(">>>>> Stage one started")
        get_data(config_path = parsed_args.config)
        logging.info("Stage one completed all the data are saved in local >>>>>")
    except Exception as e:
        logging.exception(e)
        raise e
     
    