import sys
import os
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

    def _read_pid(self):
        try:
            with open(self._pidfile, 'r') as f:
                return int(f.read().strip())
        except (IOError, OSError, ValueError):
            return None

    def _is_running(self):
        pid = self._read_pid()
        if pid is None:
            return False
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True

    def start(self):
        # if daemon is started throw an error
        if os.path.exists(self._pidfile):
            if self._is_running():
                print("[ERROR] FileWatcher is already started")
                exit(12)
            # stale pidfile left by a crash: clean it up and start normally
            print("[WARNING] Removing stale pidfile")
            os.remove(self._pidfile)
        print("[INFO] Start of FileWatcher")
        # create and switch to daemon thread
        self._daemonize()

        # run the body of the daemon
        self.launch()


    def stop(self):
        # check the pidfile existing
        if os.path.exists(self._pidfile):
            pid = self._read_pid()

            # remove the pidfile
            os.remove(self._pidfile)

            # kill daemon
            if pid is not None:
                try:
                    os.kill(pid, SIGTERM)
                except ProcessLookupError:
                    print("[WARNING] FileWatcher process was not running (stale pidfile removed)")
                    return
            print("[INFO] FileWatcher is stopped")
        else:
            print("[WARNING] FileWatcher not started")

    def status(self):
        if os.path.exists(self._pidfile) and self._is_running():
            print("[INFO] FileWatcher is running")
        else:
            print("[WARNING] FileWatcher not started")

    def restart(self):
        self.stop()
        self.start()