from codecs import register
from unittest import TestCase

from scrapy.settings import Settings
from unittest.mock import MagicMock, patch

import scrapter.updater

class SpiderExample:

    def __init__(self):
        pass

class SpiderExampleWithLast:

    def __init__(self, last=None):
        pass

class TestUpdater(TestCase):

    def setUp(self):
        self.crawl_patcher = patch('scrapter.updater.CrawlerProcess')
        self.register_patcher = patch('scrapter.updater.MongoUpdatesRegister')
        self.crawl_mock = self.crawl_patcher.start()
        self.register_mock = self.register_patcher.start()

        spiders = ['spider1', 'spider2']
        settings = Settings({
            'SPIDERS': spiders
        })
        self.updater = scrapter.updater.Updater(settings)
        self.assertListEqual(self.updater.spiders, spiders)

    def tearDown(self):
        self.crawl_patcher.stop()
        self.register_patcher.stop()

    def test_can_start(self):
        self.updater.start()
        crawl_process = self.crawl_mock.return_value
        crawl_process.crawl.assert_any_call('spider1')
        crawl_process.crawl.assert_any_call('spider2')
        crawl_process.start.assert_called()

    def test_can_register_successful_update(self):
        register = self.register_mock.return_value
        register.start = MagicMock(return_value='1')
        self.updater.start()
        register.start.assert_called_with(['spider1', 'spider2'])
        register.succeed.assert_called_with('1')

    def test_can_check_if_accepts_last(self):
        self.assertFalse(self.updater._accepts_last(SpiderExample))
        self.assertTrue(self.updater._accepts_last(SpiderExampleWithLast))
