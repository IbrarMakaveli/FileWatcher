from filewatcher.common import parser_yaml
import logging, os

class Delete(object):

    def __init__(self,**kwargs):
        self.path_watch=kwargs.get('path_watch')
        self.delete_val_yaml()

    def delete_val_yaml(self):
        list_file = parser_yaml.get_list_file_data()
        path_file_name = parser_yaml.normalize_path(self.path_watch)

        if path_file_name not in list_file:
            logging.error("Path not found : {}".format(self.path_watch))
            return False

        os.remove(path_file_name)
        logging.info('Path is deleted in FileWatcher {}'.format(self.path_watch))
        return True
