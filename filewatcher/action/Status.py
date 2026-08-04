from common.Daemon import Daemon

class Statut(Daemon):

    def __init__(self,pid_file):
        Daemon.__init__(self, pid_file)
        self.statut()
        
    def launch(self):
        pass