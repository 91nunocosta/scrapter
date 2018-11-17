from enum import Enum

class CrawlStatus(Enum):
    STARTED = 'started'
    SUCCESS = 'success'
    FAILED = 'failed'


class Crawl:

    def __init__(self, spiders, status, start, end):
        self.spiders = spiders
        self.status = status
        self.start = start
        self.end = end

class UpdatesRegister:

    def __init__(self, config):
        self.config = config

    def open_db(self):
        pass

    def close_db(self):
        pass

    def start(self, spider):
        pass

    def fail(self, spider):
        pass

    def succeed(self, spider):
        pass

    def last(self, spider):
        pass
