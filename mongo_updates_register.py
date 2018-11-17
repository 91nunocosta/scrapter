from datetime import datetime

import pymongo

from .updates_register import Crawl, CrawlStatus, UpdatesRegister
from .mongo import ConfiguredMongoMixin


class MissingConfigurationParameter(Exception):

    def __init__(self, parameter):
        super().__init__('{} parameter is missing in the configuration.'.format(parameter))


class MongoUpdatesRegister(ConfiguredMongoMixin):

    REQUIRED_PARAMETERS = ['MONGO_HOST', 'MONGO_PORT', 'MONGO_DB']

    def __init__(self, config):
        self.config = config
        self.database = None

    def start(self, spider):
        return self.get_updates().insert_one({
            'spiders': [spider],
            'status': CrawlStatus.STARTED.value,
            'start': datetime.now()
        }).inserted_id

    def fail(self, _id):
        self.get_updates().update_one(
            {'_id': _id},
            {
                '$set': {
                    'status': CrawlStatus.FAILED.value,
                    'end': datetime.now()
                }
            }
        )

    def succeed(self, _id):
        self.get_updates().update_one(
            {'_id': _id},
            {
                '$set': {
                    'status': CrawlStatus.SUCCESS.value,
                    'end': datetime.now()
                }
            }
        )

    def last(self, spider):
        updates = self.get_updates().find({
            'spiders': spider,
            'status': CrawlStatus.SUCCESS.value
        }).sort('start', pymongo.DESCENDING).limit(1)
        if updates.count() is 0:
            return None
        update = updates[0]
        return Crawl(
            update['spiders'],
            CrawlStatus(update['status']),
            update['start'],
            update['end']
        )

    def get_updates(self):
        return self.database['updates']
