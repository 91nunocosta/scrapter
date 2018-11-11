class UpdatePipeline:

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def from_crawler(self, crawler):
        pass

    def process_item(self, item, spider):
        pass

class ReplaceMongoUpdatePipeline(UpdatePipeline):

    def open_db(self):
        pass

    def close_db(self):
        pass

    def belongs(item):
        pass

    def update(item):
        pass
