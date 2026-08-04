from watchdog.events import FileSystemEventHandler

class EventHandlerRestart(FileSystemEventHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_created(self, event):
        super(EventHandlerRestart, self).on_created(event)
        if event.is_directory==False:
            self.queue.put('Add to FileWatcher')

    def on_deleted(self, event):
        super(EventHandlerRestart, self).on_deleted(event)
        if event.is_directory==False:
            self.queue.put('Delete from FileWatcher')