from enum import Enum

from scrapy.crawler import CrawlerProcess

class UpdateStatus(Enum):
    CREATED = 'created'
    STARTED = 'started'
    SUCCESS = 'success'
    FAILED = 'failed'

class Updater:

    def __init__(self, settings):
        self.settings = settings
        self.spiders = settings.get('SPIDERS')

    def start(self):
        process = CrawlerProcess(self.settings)
        for spider in self.spiders:
            process.crawl(spider)
        process.start()
