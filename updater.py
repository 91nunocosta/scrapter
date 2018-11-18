from enum import Enum

from inspect import signature

from scrapy.crawler import CrawlerProcess

from scrapy.spiderloader import SpiderLoader

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
        self.spider_loader = SpiderLoader(settings)
        self.last = self.register.last(self.spiders)

    def start(self):
        process = CrawlerProcess(self.settings)
        for spider in self.spiders:
            kwargs = self._spider_args(spider)
            process.crawl(spider, **kwargs)
        update_id = self.register.start(self.spiders)
        process.start()
        self.register.succeed(update_id)

    def _spider_args(self, spider):
        spider_cls = self.spider_loader.load(spider)
        kwargs = {}
        if self._accepts_last(spider_cls):
            kwargs['last'] = self.last.start
        return kwargs

    def _accepts_last(self, cls):
        spider_parameters = signature(cls).parameters
        return 'last' in spider_parameters
