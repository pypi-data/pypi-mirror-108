from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer


class FileMonitor:
    """Creates an observer thread that is watching directories and dispatches callback calls."""

    def __init__(self, monitorpaths, callback):
        self.monitorpaths = monitorpaths
        self.callback = callback

    def _handler(self, *args, **kwargs):
        self.callback()

    def start(self):
        self.event_handler = LoggingEventHandler()

        self.event_handler.on_created = self._handler
        self.event_handler.on_deleted = self._handler
        self.event_handler.on_modified = self._handler

        self.observer = Observer()

        for path in self.monitorpaths:
            self.observer.schedule(self.event_handler, path, recursive=True)

        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()
