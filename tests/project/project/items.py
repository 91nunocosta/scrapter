# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapter
import scrapy


class ProjectItem(scrapter.UpdatableItem):
    collection = 'items'

    name = scrapy.Field(key=True)
    category = scrapy.Field()
    last = scrapy.Field()
