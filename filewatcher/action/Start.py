from filewatcher.common.FileHandle import FileHandle
import logging
import time, re
import os
import queue
from threading import Thread
from filewatcher.common.EventHandlerQueue import EventHandlerQueue
from filewatcher.common.EventHandlerRestart import EventHandlerRestart
from watchdog.observers import Observer
from filewatcher.common import parser_yaml
from logging.handlers import TimedRotatingFileHandler
from filewatcher.common.Daemon import Daemon
from filewatcher.config.Config import Config

class Start(Daemon):

    def __init__(self,args,pid_file):
        self.is_force = args.force
        self.worker=int(args.worker)
        Daemon.__init__(self, pid_file)
        if args.force==False:
            self.start()
        if args.force==True:
            self.restart()

    def init_daemon_logger(self):
        config = Config().get_config()
        rootLogger = logging.getLogger()
        handler = TimedRotatingFileHandler("{0}/{1}".format(config['logs']['path'], config['logs']['defaultFile']), when="midnight", interval=1)
        log_level = logging.getLevelName(config['logs']['logLevel'])
        handler.setLevel(log_level)
        logFormatter = logging.Formatter(config['logs']['logMessage'],config['logs']['logFormat'])
        handler.setFormatter(logFormatter)

        # rotated files are suffixed with the day they cover
        handler.suffix = "%Y%m%d"
        handler.extMatch = re.compile(r"^\d{8}$")

        rootLogger.addHandler(handler)
        print('[INFO] Log output : {}/{}'.format(config['logs']['path'], config['logs']['defaultFile']))

    def launch(self):
        self.init_daemon_logger()
        logging.info('START Init Config : {}'.format(str(self.__dict__)))

        # Create the two queues
        my_q_event = queue.Queue()
        my_q_restart = queue.Queue()
        num_workers = self.worker
        # Create the worker threads
        pool_thread = [Thread(target=self.call_filecheck, args=(my_q_event,)) for i in range(num_workers)]
        for thread in pool_thread:
            thread.daemon = True
            thread.start()
        self.run_file_observe(False,my_q_event,my_q_restart)

    def run_file_observe(self,is_auto,my_q_event,my_q_restart):
        data_in = parser_yaml.get_read_yaml()
        data_path_file = parser_yaml.get_data_path_file()
        list_path = []

        for val in data_in:
            if os.access(val['path_watch'], os.R_OK) and os.access(val['path_watch'], os.W_OK) and os.access(val['path_watch'], os.X_OK):
                if is_auto==False:
                    self.init_launch(my_q_event,val['path_watch'])
                list_path.append(val['path_watch'])
            else:
                logging.error("Unable to read path : {}".format(val))

        observer = Observer()

        for val in list_path:
            logging.info("FileWatcher on : {}".format(val))
            observer.schedule(
                EventHandlerQueue(my_q_event,val),
                path=val)

        observer.schedule(
                EventHandlerRestart(my_q_restart),
                path=data_path_file)

        observer.start()

        while my_q_restart.empty():
            time.sleep(1)
        event = my_q_restart.get()
        my_q_restart.task_done()
        observer.stop()
        logging.warning("Restart of FileWatcher : {}".format(event))
        self.run_file_observe(True,my_q_event,my_q_restart)
        observer.join()

    def init_launch(self, my_q_event, path_watch):
        list_files = [os.path.join(path_watch, f) for f in os.listdir(path_watch) if os.path.isfile(os.path.join(path_watch, f))]
        if len(list_files)==0:
            return False
        try:
            path_last_file = max(list_files, key=os.path.getctime)
            my_q_event.put((path_last_file,path_watch))
        except Exception as e:
            logging.error(e)

    def call_filecheck(self, my_q_event):
        while True:
            file_path, path_watch = my_q_event.get()
            logging.info("File found : {}".format(file_path))

            try:
                # wait until the file stops growing before handling it
                ts_now = -1
                while ts_now != os.stat(file_path).st_mtime:
                    ts_now = os.stat(file_path).st_mtime
                    time.sleep(2)
            except (OSError, ValueError, IOError) as e:
                time.sleep(5)
                logging.warning('File disappeared/renamed - try to relaunch | msg : {}'.format(e))
                self.init_launch(my_q_event,path_watch)
                continue
            except Exception as e:
                logging.error(e)
                continue

            path_normalize = parser_yaml.normalize_path(path_watch)
            val_file = parser_yaml.get_read_single_yaml(path_normalize)
            FileHandle(file_path,val_file['file_pattern'],val_file['min_size'],val_file['command'],val_file['timewait'])
            my_q_event.task_done()
