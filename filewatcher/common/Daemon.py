import sys
import os
import logging
from signal import SIGTERM
from abc import ABCMeta, abstractmethod

class Daemon(object):
    __metaclass__ = ABCMeta

    def __init__(self, pidfile):
        self._pidfile = pidfile

    @abstractmethod
    def launch(self):
        pass

    def _daemonize(self):
        # decouple threads
        pid = os.fork()

        # stop first thread
        if pid > 0:
            sys.exit(0)

        # write pid into a pidfile
        with open(self._pidfile, 'w') as f:
            print(os.getpid(), file=f)

    def start(self):
        # if daemon is started throw an error
        if os.path.exists(self._pidfile):
            print("[ERROR] FileWatcher is already start")
            exit(12)
        print("[INFO] Start of FileWatcher")
        # create and switch to daemon thread
        self._daemonize()

        # run the body of the daemon
        self.launch()


    def stop(self):
        # check the pidfile existing
        if os.path.exists(self._pidfile):
            # read pid from the file
            with open(self._pidfile, 'r') as f:
                pid = int(f.read().strip())

            # remove the pidfile
            os.remove(self._pidfile)

            # kill daemon
            os.kill(pid, SIGTERM)
            print("[INFO] FileWatcher is stop")
        else:
            print("[WARNING] FileWatcher not started")

    def statut(self):
        if os.path.exists(self._pidfile):
            print("[INFO] FileWatcher is already start")
        else:
            print("[WARNING] FileWatcher not started")

    def restart(self):
        self.stop()
        self.start()