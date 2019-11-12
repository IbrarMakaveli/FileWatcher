import os
import logging
import re, shlex
import time, datetime
import humanfriendly
import subprocess

class FileHandle(object):

    def __init__(self,path_file,file_pattern,min_size,command,timewait):
        self.path_file = path_file
        self.file_pattern = file_pattern
        self.min_size = min_size
        self.command = command
        self.timewait = timewait
        self.run_check()

    def run_check(self):
        logging.info("Demarrage du FileCheck config : {}".format(str(self.__dict__)))
        is_checked = self.is_file_checked(self.path_file)
        if is_checked:
            self.run_command()

    def run_command(self):
        if self.timewait!="00:00:00":
            logging.info("Attente pendant : {}".format(self.timewait))
            h,m,s = self.timewait.split(':')
            time.sleep(int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds()))

        cmd_run_boa = shlex.split(self.command)
        logging.info('Run command : {}'.format(self.command))
        try:
            p = subprocess.Popen(cmd_run_boa, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            return_code = p.wait()
        except Exception as e:
            logging.error(e)
            return False

        if return_code==0:
            logging.info("Finish with SUCCESS, return code : {}".format(return_code))
        else:
            logging.error(err)
            logging.error("Finish with ERROR, return code : {}".format(return_code))
        return True

    def is_file_checked(self,path_file):
        file_size = os.stat(path_file).st_size 
        if humanfriendly.parse_size(self.min_size) > file_size:
            logging.warning("Taille du fichier trop petite par rapport au min_size : {}".format(self.min_size))
            return False
        elif bool(re.search(self.file_pattern,path_file.split(os.path.sep)[-1]))==False:
            logging.warning("Fichier ne match pas avec le pattern_file : {}".format(self.file_pattern))
            return False
        return True