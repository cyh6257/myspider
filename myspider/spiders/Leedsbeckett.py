# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider.items import HooliItem
from myspider.hooli_mode import find_fee,clear_long_text,get_index
import re

class LeedsbeckettSpider(CrawlSpider):
    name = 'Leedsbeckett'
    allowed_domains = ['leedsbeckett.ac.uk']
    start_urls = ['https://courses.leedsbeckett.ac.uk/search/courseresults/?q=&year=&level=0&startdates=&attendances=Full-time%3BSandwich&semester=&ukeuinternationalreq=&page=']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3/a'), follow=False, callback='parse_item'),
    )

    def parse_item(self, response):
        print('----------------',response)

        item=HooliItem()
        degree_type=response.xpath('//div[@class="course-hero__label"]//text()').extract()
        programme=response.xpath('//h1[@class="course-hero__title"]//text()').extract()
        #课程方向
        #//div[@class="course-hero__labels"]//text()

        mode='Full-time'

        text1=response.xpath('//div[@class="course-hero__options course-options js-course_options"]//text()').extract()
        if '\r\n                    Duration\r\n                ' in text1:
            index_dur=get_index(text1,'\r\n                    Duration\r\n                ')
            duration=text1[index_dur+2].strip()
        else:
            duration=''
        if '\r\n                    Main Location\r\n                ' in text1:
            index_lo=get_index(text1,'\r\n                    Main Location\r\n                ')
            location=text1[index_lo+2].strip()
        else:
            location=''
        start_date=re.findall('\d{1,2}\s[a-zA-Z]*\s\d{4}',''.join(text1))
        start_date=list(set(start_date))
        start_date=','.join(start_date)

        overview=response.xpath('//section[@id="overview_block"]//div[@class="tabs__panels"]//text()').extract()
        overview=clear_long_text(overview)

        entry_requirements=response.xpath('//section[@id="requirements_block"]//div[@class="tabs__panels"]/div[2]//text()').extract()
        entry_requirements=clear_long_text(entry_requirements)

        IELTS=re.findall('IELTS\s\d.\d[\sa-zA-Z]*\d.\d',entry_requirements)
        IELTS=list(set(IELTS))
        IELTS=''.join(IELTS)

        career=response.xpath('//section[@id="careers_block"]//div[@class="tabs__panels"]//text()').extract()
        career=clear_long_text(career)
        modules=response.xpath('//section[@id="learning_block"]//div[@class="tabs__panels"]//text()').extract()
        modules=clear_long_text(modules)

        tuition_fee=find_fee(''.join(response.xpath('//div[@class="tabs__panels"]//text()').extract()))
        # print(tuition_fee)

        programme=''.join(programme)
        degree_type=''.join(degree_type)

        item["university"] = 'Leeds Beckett University'
        item["location"] = location
        item["department"] = ''
        item["programme"] = programme
        item["ucas_code"] = ''
        item["degree_type"] = degree_type
        item["mode"] = mode
        item["overview"] = overview
        item["IELTS"] = IELTS
        item["TOEFL"] = ''
        item["Alevel"] = ''
        item["IB"] = ''
        item["teaching_assessment"] = ''
        item["career"] = career
        item["tuition_fee"] = tuition_fee
        item["modules"] = modules
        item["duration"] = duration
        item["start_date"] = start_date
        item["deadline"] = ''
        item["entry_requirements"] = entry_requirements
        item["url"] = response.url
        item["how_to_apply"] = ''

        # print(item)