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
            self.queue.put('Ajout de filewatcher')

    def on_deleted(self, event):
        super(EventHandlerRestart, self).on_deleted(event)
        if event.is_directory==False:
            self.queue.put('Suppression de filewatcher')