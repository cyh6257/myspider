# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider.items import HooliItem
from myspider.hooli_mode import find_fee_s,clear_long_text,get_index
import re

class WrexhamglyndwrSpider(CrawlSpider):
    name = 'WrexhamGlyndwr'
    allowed_domains = ['www.glyndwr.ac.uk']
    start_urls = ['https://www.glyndwr.ac.uk/en/Undergraduatecourses/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//dd[@id="accordion"]/ul/li/a'), follow=False,callback='parse_item'),
    )

    def parse_item(self, response):
        print('----------------',response.url)
