from datetime import datetime, timedelta
from unittest import TestCase

import mongomock

import scrapter.pipelines
from scrapter import pipelines
from scrapter.mongo import ConfiguredMongoMixin

from scrapy import Field, Item, Spider
from scrapy.crawler import Crawler
from scrapy.settings import Settings

class SpiderExample(Spider):
    pass

class UpdatePipelineExample(scrapter.pipelines.UpdatePipeline):

    parameters = ['p1', 'p2', 'p3']

    def __init__(self, config):
        super().__init__(config)
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
        self.update_pipeline = UpdatePipelineExample({})

    def test_can_be_created_from_crawler(self):
        config = {
            'p1': 'v1',
            'p2': 'v2',
            'p3': 'v3'
        }
        settings = Settings(config)
        crawler = Crawler(SpiderExample, settings)
        pipeline = UpdatePipelineExample.from_crawler(crawler)
        self.assertDictEqual(pipeline.config, config)

    def test_can_open_spider(self):
        self.update_pipeline.open_spider(None)
        self.assertTrue(self.update_pipeline.opened)

    def test_can_close_spider(self):
        self.update_pipeline.close_spider(None)
        self.assertTrue(self.update_pipeline.closed)

    def test_can_process_item(self):
        self.update_pipeline.process_item('item')
        self.assertEqual(self.update_pipeline.updated, 'item')


class ExampleItem(Item):
    collection = 'items'
    field1 = Field(key=True)
    field2 = Field()
    field3 = Field()

    def key(self):
        return ['field1', 'field2']

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

    def test_can_get_filter(self):
        item = ExampleItem()
        item['field1'] = 1
        item['field2'] = 2
        item['field3'] = 3
        self.assertDictEqual(self.pipeline._filter(item), {'field1': 1, 'field2': 2})

    @mongomock.patch(servers=(('mongodb', 2701),))
    def test_can_update(self):
        client = mongomock.MongoClient('mongodb', port=27017)
        self.pipeline.database = client['db']
        item = ExampleItem()
        item['field1'] = '1'
        item['field2'] = 'value'
        self.pipeline.update(item)
        saved_item = self.pipeline.database['items'].find_one({'field1': '1'})
        self.assertEqual(saved_item['field1'], '1')
        self.assertEqual(saved_item['field2'], 'value')
        self.assertAlmostEqual(saved_item['_updated'], datetime.now(), delta=timedelta(seconds=1))
