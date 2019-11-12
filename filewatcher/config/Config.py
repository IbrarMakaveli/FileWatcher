import yaml
import os, datetime, logging
import re
import humanfriendly
import getpass

class Config(object):

    def get_config(self):
        root_dir = os.path.dirname(os.path.abspath(__file__)) 
        config_path = os.path.join(root_dir, 'config.yaml')
        with open(config_path, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            return cfg

    def check_config(self,**kwargs):
        path_watch=kwargs.get('path_watch')
        file_pattern=kwargs.get('file_pattern', None)
        min_size=kwargs.get('min_size', None)
        timewait=kwargs.get('timewait', None)

        if os.path.isdir(path_watch)==False:
            logging.error("Chemin n'existe pas : {}".format(path_watch))
            exit(12)

        if os.access(path_watch, os.R_OK)==False or os.access(path_watch, os.W_OK)==False or os.access(path_watch, os.X_OK)==False:
            username = getpass.getuser()
            logging.error("Utilisateur '{}' n'a pas les droits (rwx) au chemin : {}".format(username,path_watch))
            exit(12)
        
        try:
            if timewait is not None:
                datetime.datetime.strptime(timewait, "%H:%M:%S")
        except Exception as e:
            logging.error("Format timewait incorrect (HH:MM:SS) : {}".format(timewait))
            logging.error(e)
            exit(12)

        try:
            if file_pattern is not None:
                re.compile(file_pattern)
        except Exception as e:
            logging.error("Format du regex incorrect (regex python sur google) : {}".format(file_pattern))
            logging.error(e)
            exit(12)
            
        try:
            if min_size is not None:
                humanfriendly.parse_size(min_size)
        except Exception as e:
            logging.error("Format du minsize incorrect (B,KB,MB,GB,TB): {}".format(min_size))
            logging.error(e)
            exit(12)
    