from abc import ABC, abstractmethod

from scrapter.mongo import ConfiguredMongoMixin

class UpdatePipeline(ABC):

    def open_spider(self, spider):
        self.open_db()

    def close_spider(self, spider):
        self.close_db()

    def process_item(self, item):
        self.update(item)

    @abstractmethod
    def open_db(self):
        pass

    @abstractmethod
    def close_db(self):
        pass

    @abstractmethod
    def update(self, item):
        pass


class MongoUpdatePipeline(UpdatePipeline, ConfiguredMongoMixin):

    def get_collection(self, item):
        pass

class ReplaceMongoUpdatePipeline(MongoUpdatePipeline):
    pass
