from watchdog.events import FileSystemEventHandler

class EventHandlerQueue(FileSystemEventHandler):
    def __init__(self, queue, path_watch):
        self.queue = queue
        self.path_watch = path_watch

    def on_created(self, event):
        super(EventHandlerQueue, self).on_created(event)
        if event.is_directory==False:
            self.queue.put((event.src_path, self.path_watch))
