from datetime import datetime
from symbol import parameters

from scrapter.mongo import ConfiguredMongoMixin


class UpdatePipeline():

    @classmethod
    def from_crawler(cls, crawler):
        config = {}
        for parameter in cls.parameters:
            config[parameter] = crawler.settings.get(parameter)
        return cls(config)

    def __init__(self, config):
        self.config = config

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

    def __init__(self, config):
        super().__init__(config)

    def _filter(self, item):
        return {key: item[key] for key in item.key()}

    def update(self, item):
        collection = self.database[item.collection]
        _filter = self._filter(item)
        collection.delete_many(_filter)
        updated_item = dict(item)
        updated_item['_updated'] = datetime.now()
        collection.insert_one(updated_item)
