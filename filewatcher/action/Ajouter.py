import common.parser_yaml as parser_yaml
import datetime
import logging, os
from config.Config import Config

class Ajouter(object):

    def __init__(self,**kwargs):
        self.path_watch=kwargs.get('path_watch')
        self.file_pattern=kwargs.get('file_pattern', None)
        self.min_size=kwargs.get('min_size', None)
        self.command=kwargs.get('command', None)
        self.timewait=kwargs.get('timewait', None)
        self.add_val_yaml()

    def add_val_yaml(self):

        Config().check_config(path_watch=self.path_watch,file_pattern=self.file_pattern,min_size=self.min_size,timewait=self.timewait)

        path_file_name = parser_yaml.normalize_path(self.path_watch)

        new_val = {'path_watch':self.path_watch,'file_pattern':self.file_pattern,'min_size':self.min_size,'command':self.command,'timewait':self.timewait}

        parser_yaml.set_write_yaml(path_file_name,new_val)

        logging.info('Add new path to watch : {}'.format(self.path_watch))
        
        return True