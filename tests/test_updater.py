from unittest import TestCase
from unittest.mock import patch, MagicMock

from scrapy.settings import Settings

import scrapter.updater

class TestUpdater(TestCase):

    def setUp(self):
        self.crawl_patcher = patch('scrapter.updater.CrawlerProcess')
        self.crawl_mock = self.crawl_patcher.start()

        spiders = ['spider1', 'spider2']
        settings = Settings({
            'SPIDERS': spiders
        })
        self.updater = scrapter.updater.Updater(settings)
        self.assertListEqual(self.updater.spiders, spiders)

    def tearDown(self):
            # self.crawl_patcher.stop()
        pass

    def test_can_start(self):
        self.updater.start()
        crawl_process = self.crawl_mock.return_value
        crawl_process.crawl.assert_any_call('spider1')
        crawl_process.crawl.assert_any_call('spider2')
        crawl_process.start.assert_called()
