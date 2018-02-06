# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider.items import HooliItem
from myspider.hooli_mode import find_fee_s,clear_long_text,get_index
import re

class UosSpider(CrawlSpider):
    name = 'Uos'
    allowed_domains = ['www.uos.ac.uk']
    start_urls = ['https://www.uos.ac.uk/course-list?search_api_views_fulltext=&field_study_mode%5B0%5D=41&type%5B0%5D=ucs_ug_courses&page=']

    rules = (
        Rule(LinkExtractor(allow=r'page=\d*'),follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="view-content"]/div/div/a'), follow=False, callback='parse_item'),
    )


    def parse_item(self, response):
        print('----------------',response.url)

        programme=response.xpath('//h1//text()').extract()
        programme=''.join(programme)
        # print(programme)
        text1=response.xpath('//div[@class="l-node--top-info"]//text()').extract()
        # print(text1)

        if 'UCAS code:\xa0' in text1:
            index_ucas=text1.index('UCAS code:\xa0')
            ucas_code=text1[index_ucas+3]
        else:
            ucas_code=''
        if 'Location:\xa0' in text1:
            index_lo=text1.index('Location:\xa0')
            location=text1[index_lo+3]
        else:
            location=''

        duration=re.findall('.*year[a-z\s]*full-time',''.join(text1))
        duration=''.join(duration).strip().replace('full-time','')


        overview=response.xpath('//div[@id="group-description"]//text()').extract()
        overview=clear_long_text(overview)

        modules=response.xpath('//div[@id="group-duration-modules"]//text()').extract()
        modules=clear_long_text(modules)
        # print(modules)

        career=response.xpath('//div[@id="group-career"]//text()').extract()
        career=clear_long_text(career)


        fees=response.xpath('//div[@id="group-fees"]//text()').extract()
        tuition_fee=find_fee_s(fees)
        # print(tuition_fee)

        #//div[@id="group-entry-requirements"]//text()

        entry_requirements=response.xpath('//div[@id="group-entry-requirements"]//text()').extract()
        entry_requirements=clear_long_text(entry_requirements)

        mode='full-time'
        university='University of Suffolk'
        text2=response.xpath('//div[@id="group-entry-requirements"]//text()').extract()
        text2=''.join(text2)
        IELTS=re.findall('IELTS[\sa-zA-Z]*\d\.\d[\s\w\(\)\.]*',text2)
        IELTS=''.join(IELTS)
