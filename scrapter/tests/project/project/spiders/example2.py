# -*- coding: utf-8 -*-
import scrapy

from project.items import ProjectItem

from datetime import datetime

class ExampleSpider(scrapy.Spider):
    name = 'example2'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, response):
        pass
