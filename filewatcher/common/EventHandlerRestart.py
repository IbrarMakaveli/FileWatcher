from watchdog.events import FileSystemEventHandler
import logging
import os, subprocess, sys
from config.Config import Config

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
            self.queue.put('Delete to Filewatcher')