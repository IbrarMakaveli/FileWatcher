import common.parser_yaml as parser_yaml
import logging, os
from config.Config import Config

class Supprimer(object):

    def __init__(self,**kwargs):
        self.path_watch=kwargs.get('path_watch')
        self.supp_val_yaml()

    def supp_val_yaml(self,**kwargs):
        list_file = parser_yaml.get_list_file_data()
        path_file_name = parser_yaml.normalize_path(self.path_watch)

        if path_file_name not in list_file:
            logging.error("Ce chemin n'existe pas deja dans la config : {}".format(self.path_watch))
            return False

        os.remove(path_file_name)
        logging.info('Suppression du chemin dans le filewatcher {}'.format(self.path_watch))
        return True

        