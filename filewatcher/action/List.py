import common.parser_yaml as parser_yaml
import datetime
import logging, os, pprint
from collections import OrderedDict
from config.Config import Config
from tabulate import tabulate

class Lister(object):

    def __init__(self,**kwargs):
        self.list_path_watch=kwargs.get('list_path_watch',None)
        self.output_path_watch()

    def output_path_watch(self):
        list_file = parser_yaml.get_list_file_data()
        output_dataset = []
        
        if self.list_path_watch is None:
            for path_file in list_file:
                output_dataset.append(self.order_append_dict(path_file))
        else:
            data_path = parser_yaml.get_data_path_file()
            for path_in in self.list_path_watch:
                path_file_name = parser_yaml.normalize_path(path_in).replace('.yaml','')
                for path_file in list_file:
                    if path_file_name.replace(data_path,'').replace(os.path.sep,'') in path_file.replace(data_path,'').replace(os.path.sep,''):
                        output_dataset.append(self.order_append_dict(path_file))
        
        print(tabulate(output_dataset, headers='keys', tablefmt='psql'))


    def order_append_dict(self, path_file):
        dict_config = parser_yaml.get_read_single_yaml(path_file)
        my_ord_dict = OrderedDict()
        my_ord_dict['path_watch'] = dict_config['path_watch']
        my_ord_dict['command'] = dict_config['command']
        my_ord_dict['min_size'] = dict_config['min_size']
        my_ord_dict['file_pattern'] = dict_config['file_pattern']
        my_ord_dict['timewait'] = dict_config['timewait']
        return my_ord_dict
