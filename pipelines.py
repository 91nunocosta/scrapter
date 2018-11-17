from datetime import datetime

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

    def _filter(self, item):
        return {key: item[key] for key in item.key()}

    def update(self, item):
        collection = self.database[item.collection]
        _filter = self._filter(item)
        collection.delete_many(_filter)
        updated_item = dict(item)
        updated_item['_updated'] = datetime.now()
        collection.insert_one(updated_item)
