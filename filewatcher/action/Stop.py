from common.Daemon import Daemon

class Stop(Daemon):

    def __init__(self,pid_file):
        Daemon.__init__(self, pid_file)
        self.stop()
        
    def launch(self):
        pass