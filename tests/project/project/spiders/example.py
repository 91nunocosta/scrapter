# -*- coding: utf-8 -*-
import scrapy

from project.items import ProjectItem

from datetime import datetime

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def __init__(self, last=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last = last

    def parse(self, response):
        yield ProjectItem(name='updated_item', last=self.last)
        yield ProjectItem(name='new_item')
