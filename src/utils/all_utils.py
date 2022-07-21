from email import contentmanager
import yaml
import os
import json
from tqdm import tqdm
import shutil
import logging
import time



def read_yaml(path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
        logging.info(f"yaml file: {path_to_yaml} loaded successfully")
    return content


def create_directory(dirs: list):
    for dir_path in dirs:
       os.makedirs(dir_path, exist_ok=True) 
       logging.info(f"Directory is created at {dir_path}")
       

def save_local_df(data, data_path):
    data.to_csv(data_path, index = False)
    logging.info(f"Data is saved at {data_path}")
    
    
def save_reports(report: dict, report_path: str):
    with open(report_path, 'w') as f:
        json.dump(report, f, indent = 4)
    logging.info(f"Reports are saved at {report_path}")   
    
    
def copy_file(source_download_dir, local_data_dir):
    list_of_files = os.listdir(source_download_dir)
    N = len(list_of_files)
    for file in tqdm(list_of_files, total = N, desc = f"coping files from {source_download_dir} to {local_data_dir}", colour = 'green'):
        src = os.path.join(source_download_dir, file)
        dest = os.path.join(local_data_dir, file)
        shutil.copy(src, dest) 
        
        
def get_timestamp(name):
    timestamp = time.asctime().replace("", "_").replace(":", "_")
    unique_name = f"{name}_at_{timestamp}"
    return unique_name