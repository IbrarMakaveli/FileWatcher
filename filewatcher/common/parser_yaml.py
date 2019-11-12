import yaml, os, logging, time
from datetime import datetime
from threading import RLock 
from config.Config import Config

verrou = RLock()
config = Config().get_config()
data_path_file = config['data']['path']

def get_data_path_file():
    return data_path_file

def get_list_file_data():
    return [os.path.join(data_path_file, f) for f in os.listdir(data_path_file) if os.path.isfile(os.path.join(data_path_file, f))]

def normalize_path(path):
    return '{}.yaml'.format(os.path.join(data_path_file, path.replace(os.path.sep, '_')))

def get_read_yaml():
    list_file = get_list_file_data()
    data_in = []

    for val in list_file:
        with verrou:
            with open(val,'r') as f:
                data_in.append(yaml.safe_load(f))
    
    return data_in

def get_read_single_yaml(path_file_name):
    val_yaml = False
    with verrou:
        with open(path_file_name,'r') as f:
            val_yaml = yaml.safe_load(f)
    return val_yaml

def set_write_yaml(path_yaml,val_yaml):
    with verrou:
        with open(path_yaml,'w') as f:
            yaml.safe_dump(val_yaml, f)
    return True