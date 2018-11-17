from abc import ABC, abstractmethod
from datetime import datetime

from pymongo import collection

from scrapter.mongo import ConfiguredMongoMixin


class UpdatePipeline():

    def open_spider(self, spider):
        self.open_db()

    def close_spider(self, spider):
        self.close_db()

    def process_item(self, item):
        self.update(item)

    def open_db(self):
        pass

    def close_db(self):
        pass

    def update(self, item):
        pass


class MongoUpdatePipeline(ConfiguredMongoMixin, UpdatePipeline):

    def __init__(self, db_config):
        self.db_config = db_config

    def update(self, item):
        collection = self.database[item.collection]
        key = item.key()
        _filter = {key: item[key]}
        delete_result = collection.delete_many(_filter)
        item['_updated'] = datetime.now()
        collection.insert_one(dict(item))
