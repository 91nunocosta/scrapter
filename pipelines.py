class UpdatePipeline:

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item):
        pass

    def open_db(self):
        pass

    def close_db(self):
        pass

    def update(self, item):
        pass


class MongoUpdatePipeline(UpdatePipeline):

    def get_collection(self, item):
        pass

class ReplaceMongoUpdatePipeline(MongoUpdatePipeline):
    pass
