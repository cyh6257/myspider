# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider.items import HooliItem
import re
import scrapy
import requests
from w3lib.html import remove_tags

class HarperadamsGSpider(CrawlSpider):
    name = 'HarperAdams_g'
    allowed_domains = ['www.harper-adams.ac.uk']
    start_urls = []
    base_url='https://www.harper-adams.ac.uk/courses/courses.cfm?q=&type=postgraduate&area=&yoe=2018&title=%s'
    Title=['A','C','E','F','I','L','M','P','R','S','V','W']
    for i in Title:
        fullurl=base_url % i
        start_urls.append(fullurl)
        rules=(
            Rule(LinkExtractor(allow='.*'), follow=False, callback='parse_item'),
        )
    def parse_item(self, response):
        print(response.url,'---------------')
        uid=response.url.split('/')[5]
        item = HooliItem()
        long_str = response.xpath('//div[@class="content-section-margin"]//text()').extract()
        index_Duration = long_str.index('Duration')
        Duration = long_str[index_Duration + 2]
        # print(Duration)
        index_startDate = long_str.index('Start date:')
        StartDate = long_str[index_startDate + 1]
        # print(StartDate)
        Course = response.url.split('/')[-1]
        Course = Course.replace('-', ' ').title()
        # print(Course)
        EntryRequirements = response.xpath('//div[@id="entry-requirements"]//text()').extract()
        EntryRequirements = ''.join(EntryRequirements).strip()

        CourseOverview = response.xpath('//div[@id="overview"]//text()').extract()
        CourseOverview = ''.join(CourseOverview).strip()
        # modules
        # Modules = response.xpath('//div[@id="modules"]//text()').extract()
        # Modules = ''.join(Modules).strip()
        base_url='https://www.harper-adams.ac.uk/shared/get-pg-route-modules.cfm?year_of_entry=2018&route=9&id=%s'
        full_url=base_url % uid
        modules=requests.get(full_url)
        modules=remove_tags(modules.content)
        modules=modules.strip().replace('Click module title to see full description:','')
        # print(modules)
        # careers
        Career = response.xpath('//div[@id="careers"]//text()').extract()
        Career = ''.join(Career).strip()
        # teaching
        Assessment = response.xpath('//div[@id="teaching"]//text()').extract()
        Assessment = ''.join(Assessment).strip()
        Master = response.xpath('//div[@class="page-heading"]/h2/text()').extract()
        Master = ''.join(Master)
        University = 'Harper Adams'
        item["university"] = University
        item["location"] = 'Newport'
        item["department"] = ''
        item["programme"] = Course
        item["ucas_code"] = ''
        item["degree_type"] =Master
        item["overview"] =CourseOverview
        item["IELTS"] = '6.0(minimum 5.5 in any component)'
        item["TOEFL"] = '80+(minimum 18 reading, 18 Listening, 22 speaking, 20 writing)'
        item["Alevel"] = ''
        item["IB"] = ''
        item["teaching_assessment"] = Assessment
        item["career"] =Career
        item["tuition_fee"] = ''
        item["modules"] =modules
        item["duration"] = Duration
        item["start_date"] = StartDate
        item["deadline"] = ''
        item["entry_requirements"] =EntryRequirements
        item["url"] = response.url
        item["Justone"] = response.url
        item["type"] = type
        if Master =="PgC":
            print(Master, 'do not need')
        else:
            yield item
    # def parse(self, response):
    #     item=HooliItem()
    #     long_str=response.xpath('//div[@class="content-section-margin"]//text()').extract()
    #     index_Duration=long_str.index('Duration')
    #     Duration=long_str[index_Duration+2]
    #     # print(Duration)
    #     index_startDate=long_str.index('Start date:')
    #     StartDate=long_str[index_startDate+1]
    #     # print(StartDate)
    #     Course=response.url.split('/')[-1]
    #     Course=Course.replace('-',' ').title()
    #     # print(Course)
    #     EntryRequirements=response.xpath('//div[@id="entry-requirements"]//text()').extract()
    #     EntryRequirements=''.join(EntryRequirements).strip()
    #
    #     CourseOverview = response.xpath('//div[@id="overview"]//text()').extract()
    #     CourseOverview = ''.join(CourseOverview).strip()
    #     #modules
    #     Modules = response.xpath('//div[@id="modules"]//text()').extract()
    #     Modules = ''.join(Modules).strip()
    #     #careers
    #     Career = response.xpath('//div[@id="careers"]//text()').extract()
    #     Career = ''.join(Career).strip()
    #     #teaching
    #     Assessment = response.xpath('//div[@id="teaching"]//text()').extract()
    #     Assessment=''.join(Assessment).strip()
    #     Master=response.xpath('//div[@class="page-heading"]/h2/text()').extract()
    #     Master=''.join(Master)
    #     University = 'Harper Adams'
    #     item["url"] = response.url
    #     item["University"] = University
    #     item["Department"] = ''
    #     item["Location"] = ''
    #     item["Course"] = Course
    #     item["CourseCode"] = ''
    #     item["Master"] = Master
    #     item["CourseOverview"] = CourseOverview
    #     item["Alevel"] = ''
    #     item["IB"] = ''
    #     item["IELTS"] = ''
    #     item["TOEFL"] = ''
    #     item["Assessment"] = Assessment
    #     item["Career"] = Career
    #     item["TuitionFee"] = ''
    #     item["Modules"] = Modules
    #     item["Duration"] = Duration
    #     item["StartDate"] = StartDate
    #     item["Deadline"] = ''
    #     item["EntryRequirements"] = EntryRequirements
    #     yield item