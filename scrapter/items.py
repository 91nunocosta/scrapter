from scrapy import Item, Field

class UpdatableItem(Item):

    _update = Field()


    def key(self):
        return [name for name, field in self.fields.items() if 'key' in field and field['key']]
