from enum import Enum

class CrawlStatus(Enum):
    STARTED = 'started'
    SUCCESS = 'success'
    FAILED = 'failed'


class Crawl:

    def __init__(self, spider):
        self.spider = spider


class UpdatesRegister:

    def __init__(self, db_config):
        self.db_config = db_config

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
