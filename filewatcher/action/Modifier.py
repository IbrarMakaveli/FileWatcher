import common.parser_yaml as parser_yaml
import logging, os
from config.Config import Config

class Modifier(object):

    def __init__(self,**kwargs):
        self.path_watch=kwargs.get('path_watch')
        self.file_pattern=kwargs.get('file_pattern', None)
        self.min_size=kwargs.get('min_size', None)
        self.command=kwargs.get('command', None)
        self.timewait=kwargs.get('timewait', None)
        self.modify_path_watch()

    def modify_path_watch(self):

        Config().check_config(path_watch=self.path_watch,file_pattern=self.file_pattern,min_size=self.min_size,timewait=self.timewait)

        list_file = parser_yaml.get_list_file_data()
        path_file_name = parser_yaml.normalize_path(self.path_watch)

        if path_file_name not in list_file:
            logging.error("Ce chemin n'existe pas deja dans la config : {} | utiliser ajouter".format(self.path_watch))
            return False

        modif_val = parser_yaml.get_read_single_yaml(path_file_name)

        if self.file_pattern is not None:
            modif_val['file_pattern'] = self.file_pattern
        if self.min_size is not None:
            modif_val['min_size'] = self.min_size
        if self.command is not None:
            modif_val['command'] = self.command
        if self.timewait is not None:
            modif_val['timewait'] = self.timewait

        parser_yaml.set_write_yaml(path_file_name,modif_val)

        logging.info('Modification du chemin dans le filewatcher {}'.format(self.path_watch))
        
        return True