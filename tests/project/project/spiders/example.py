# -*- coding: utf-8 -*-
import scrapy

from project.items import ProjectItem

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        yield ProjectItem(name='item1')
