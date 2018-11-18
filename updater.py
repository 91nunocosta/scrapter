from enum import Enum

from inspect import signature

from scrapy.crawler import CrawlerProcess

from scrapter.mongo_updates_register import MongoUpdatesRegister


class UpdateStatus(Enum):
    CREATED = 'created'
    STARTED = 'started'
    SUCCESS = 'success'
    FAILED = 'failed'


class Updater:

    def __init__(self, settings):
        self.settings = settings
        self.spiders = settings.get('SPIDERS')
        self.register = MongoUpdatesRegister(settings)

    def start(self):
        process = CrawlerProcess(self.settings)
        for spider in self.spiders:
            process.crawl(spider)
        update_id = self.register.start(self.spiders)
        process.start()
        self.register.succeed(update_id)

    def _accepts_last(self, cls):
        spider_parameters = signature(cls).parameters
        return 'last' in spider_parameters
