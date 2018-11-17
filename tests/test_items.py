from unittest import TestCase

from scrapter.items import UpdatableItem
from scrapy import Field

class ExampleUpdatableItem(UpdatableItem):

    key1 = Field(key=True)
    key2 = Field(key=True)
    field1 = Field()
    field2 = Field()

class TestUpdatableItem(TestCase):

    def test_key(self):
        item = ExampleUpdatableItem()
        self.assertListEqual(item.key(), ['key1', 'key2'])

