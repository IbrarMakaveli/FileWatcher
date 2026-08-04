from filewatcher.common.Daemon import Daemon

class Status(Daemon):

    def __init__(self,pid_file):
        Daemon.__init__(self, pid_file)
        self.status()

    def launch(self):
        pass
