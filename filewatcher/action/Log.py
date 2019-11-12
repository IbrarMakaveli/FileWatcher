import datetime, subprocess
import logging, os, pprint
from config.Config import Config

class Log(object):

    def __init__(self,args,logfile):
        self.all=args.all
        self.date=args.date
        self.logfile=logfile
        self.output_log()

    def output_log(self):
        if self.date is not None:
            try :
                with open('{}.{}'.format(self.logfile,self.date.strftime('%Y%m%d'))) as f:
                    print(f.read())
            except IOError:
                print("[ERROR] Aucune log pour la date du {}".format(self.date.strftime('%Y-%m-%d')))
        elif self.all==True:
            with open(self.logfile) as f:
                print(f.read())
        else:
            f = subprocess.Popen(['tail','-F',self.logfile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            try:
                while True:
                    print(f.stdout.readline().rstrip())
            except KeyboardInterrupt:
                print("[INFO] Exit keyboard log")