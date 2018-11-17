from unittest import TestCase

import mongomock

import scrapter.pipelines
from scrapter import pipelines
from scrapter.mongo import ConfiguredMongoMixin


class UpdatePipelineExample(scrapter.pipelines.UpdatePipeline):

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

    @mongomock.patch(servers=(('mongodb', 27017),))
    def setUp(self):
        import scrapter.pipelines
        db_config = {
            'MONGO_HOST': 'mongo',
            'MONGO_PORT': 27017,
            'MONGO_DB': 'db'
        }
        self.pipeline = scrapter.pipelines.MongoUpdatePipeline(db_config)
        self.assertDictEqual(self.pipeline.db_config, db_config)

    @mongomock.patch(servers=(('mongodb', 27017),))
    def test_can_open_db(self):
        self.pipeline.open_spider(None)
        self.assertTrue(self.pipeline.database)
        self.assertIsInstance(self.pipeline.database, mongomock.database.Database)
