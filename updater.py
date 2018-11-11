from enum import Enum

class UpdateStatus(Enum):
    CREATED = 'created'
    STARTED = 'started'
    SUCCESS = 'success'
    FAILED = 'failed'

class Updater:

    def __init__(self, settings):
        self.settings = settings
        self.pipelines = self.__get_spiders(settings)

    def __get_spiders(self, settings):
        return []

    def start(self):
        pass
