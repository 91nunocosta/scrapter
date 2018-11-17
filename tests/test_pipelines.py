from unittest import TestCase
from scrapter.pipelines import UpdatePipeline, MongoUpdatePipeline, ReplaceMongoUpdatePipeline

class UpdatePipelineExample(UpdatePipeline):

    def __init__(self):
        super().__init__()
        self.opened = False
        self.closed = False
        self.updated = None

    def open_db(self):
        self.opened = True

    def close_db(self):
        self.closed = True

    def update(self, item):
        self.updated = item


class TestUpdatePipeline(TestCase):

    def setUp(self):
        self.update_pipeline = UpdatePipelineExample()

    def test_can_open_spider(self):
        self.update_pipeline.open_spider(None)
        self.assertTrue(self.update_pipeline.opened)

    def test_can_close_spider(self):
        self.update_pipeline.close_spider(None)
        self.assertTrue(self.update_pipeline.closed)

    def test_can_process_item(self):
        self.update_pipeline.process_item('item')
        self.assertEqual(self.update_pipeline.updated, 'item')

class TestMongoUpdatePipeline(TestCase):
    pass


class TestReplaceMongoUpdatePipeline(TestCase):
    pass
