from unittest import TestCase

from scrapter.updater import Updater

from scrapy.settings import Settings

class TestUpdater(TestCase):

    def setUp(self):
        spiders = ['spider1', 'spider2']
        settings = Settings({
            'SPIDERS': spiders
        })
        self.updater = Updater(settings)
        self.assertListEqual(self.updater.spiders, spiders)

    def test_can_start(self):
        pass
