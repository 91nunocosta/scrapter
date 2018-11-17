from enum import Enum

class UpdateStatus(Enum):
    CREATED = 'created'
    STARTED = 'started'
    SUCCESS = 'success'
    FAILED = 'failed'

class Updater:

    def __init__(self, settings):
        self.spiders = settings.get('SPIDERS')

    def start(self):
        pass
