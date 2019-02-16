from enum import Enum
from inspect import signature
from platform import processor

from scrapy.crawler import CrawlerProcess
from scrapy.spiderloader import SpiderLoader

from scrapter.mongo_updates_register import MongoUpdatesRegister


class UpdateStatus(Enum):
    CREATED = 'created'
    STARTED = 'started'
    SUCCESS = 'success'
    FAILED = 'failed'

class MissingSetting(Exception):
    
    def __init__(self, parameter):
        super().__init__('{} setting is missing.'.format(parameter))

class Updater:

    REQUIRED_PARAMETERS = ['MONGO_HOST', 'MONGO_PORT', 'MONGO_DB', 'SPIDERS']

    def __init__(self, settings):
        self.__validate_settings(settings)
        self.settings = settings
        self.spiders = settings.get('SPIDERS')
        self.register = MongoUpdatesRegister(settings)
        self.register.open_db()
        self.spider_loader = SpiderLoader(settings)
        self.last = self.register.last(self.spiders)

    def __validate_settings(self, settings):
        for parameter in Updater.REQUIRED_PARAMETERS:
            if parameter not in settings:
                raise MissingSetting(parameter)

    def run(self):
        process = CrawlerProcess(self.settings)
        for spider in self.spiders:
            kwargs = self._spider_args(spider)
            process.crawl(spider, **kwargs)
        update_id = self.register.start(self.spiders)
        process.start()
        if self._failed(process):
            self.register.fail(update_id)
        else:
            self.register.succeed(update_id)

    def _spider_args(self, spider):
        spider_cls = self.spider_loader.load(spider)
        kwargs = {}
        if self._accepts_last(spider_cls):
            kwargs['last'] = self.last.start
        return kwargs

    def _accepts_last(self, cls):
        spider_parameters = signature(cls.__init__).parameters
        return 'last' in spider_parameters

    def _failed(self, process):
        finish_reasons = [crawler.stats.get_value('finish_reason') for crawler in process.crawlers]
        return any(reason != 'finished' for reason in finish_reasons)
