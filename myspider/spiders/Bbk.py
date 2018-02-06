# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider.items import HooliItem
from myspider.hooli_mode import find_fee_s,clear_long_text,get_index
import re

class BbkSpider(CrawlSpider):
    name = 'Bbk'
    allowed_domains = ['www.bbk.ac.uk']
    start_urls = ['http://www.bbk.ac.uk/study/course_search?q=%2A&lvl=ug&yr=2018&b_start:int=0']

    rules = (
        Rule(LinkExtractor(allow='b_start:int=\d+'),follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ol/li/a'),follow=False,callback='parse_item'),
    )

    def parse_item(self, response):
        print('----------------',response.url)
        item=HooliItem()
        text1=response.xpath('//div[@class="major-intro"]//text()').extract()
        index_st=get_index(text1,'Start date')
        start_date=text1[index_st+2].strip()
        index_lo=get_index(text1,'Location')
        location=text1[index_lo+3].strip()
        if 'UCAS Code' in text1:
            index_ucas=get_index(text1,'UCAS Code')
            ucas_code=text1[index_ucas+2].strip()
        else:
            ucas_code=''
        programme=text1[3].strip()
        programme=programme.split(':')[0]
        degree_type=re.findall('\(.*\)',programme)
        degree_type=''.join(degree_type)

        if 'Duration' in text1:
            index_dur=get_index(text1,'Duration')
            durations=text1[index_dur+3]
        else:
            durations=''
        duration=re.findall('(?i)[\sa-zA-Z]*year[\sa-zA-Z]*full-time',durations)
        mode=re.findall('full-time',durations)
        duration=''.join(duration)
        mode=''.join(mode)

        overview=response.xpath('//div[@class="row column max-medium"]/div/p//text()|//div[@class="row column max-medium"]/div/ul//text()').extract()
        overview=clear_long_text(overview)
        modules=response.xpath('//div[@id="courseStructure"]//text()').extract()
        modules=clear_long_text(modules)

        entry_requirements=response.xpath('//div[@class="row column max-xxlarge"]//text()').extract()
        title=response.xpath('//div[@class="column medium-10 large-8"]//ul/li/a//text()').extract()
        title=clear_long_text(title)
        entry_requirements=clear_long_text(entry_requirements)
        entry_requirements=title+'\n'+entry_requirements

        IELTS=re.findall('\d\.\d[\sa-zA-Z\,]*\d\.\d',entry_requirements)
        IELTS=''.join(IELTS)
        tuition_fee=find_fee_s(entry_requirements)
        programme = programme.replace(degree_type,'')
        item["university"] = 'Birkbeck University of London'
        item["location"] =location
        item["department"] = ''
        item["programme"] = programme
        item["ucas_code"] = ucas_code
        item["degree_type"] = degree_type
        item["mode"] = mode
        item["overview"] = overview
        item["IELTS"] = IELTS
        item["TOEFL"] = ''
        item["Alevel"] = ''
        item["IB"] = ''
        item["teaching_assessment"] = ''
        item["career"] = ''
        item["tuition_fee"] = tuition_fee
        item["modules"] = modules
        item["duration"] = duration
        item["start_date"] = start_date
        item["deadline"] = ''
        item["entry_requirements"] = entry_requirements
        item["url"] = response.url
        item["how_to_apply"] = ''
        item["degree_level"] = 0

        if mode =='full-time':
            # yield item
            print(item)
        else:
            print('do not need part-time')