# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider.items import HooliItem
from myspider.hooli_mode import find_fee_s,clear_long_text,get_index
import re


class CumbriaSpider(CrawlSpider):
    name = 'Cumbria'
    allowed_domains = ['www.cumbria.ac.uk']
    start_urls = ['https://www.cumbria.ac.uk/study/courses/course-search/?level=ug-full-time-degree&level=ug-sandwich-placement&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'page=\d*'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="articles-wrapper"]/article/a'), follow=False,
             callback='parse_item'),
    )

    def parse_item(self, response):
        print('--------------------',response.url)
        titles=response.xpath('//h1//text()').extract()
        titles=''.join(titles)
        degree_type=re.findall('[A-Za-z]*\s\([a-zA-Z]{0,6}\)',titles)
        degree_type=''.join(degree_type)
        programme=titles.replace(degree_type,'').strip()

        ucas_code=response.xpath('//div[@class="ucas-code"]//text()').extract()
        ucas_code=''.join(ucas_code).replace('Course code','').strip()
        # print(ucas_code)

        modules=response.xpath('//div[@id="course-outline"]//text()').extract()
        modules=''.join(modules)
        # print(modules)