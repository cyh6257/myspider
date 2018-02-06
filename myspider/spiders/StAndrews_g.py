# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider.items import HooliItem
import re

class StandrewsGSpider(CrawlSpider):
    name = 'StAndrews_g'
    allowed_domains = ['www.st-andrews.ac.uk']
    start_urls = ['https://www.st-andrews.ac.uk/subjects/']

    rules = (
        Rule(LinkExtractor(allow=(r'.*'),restrict_xpaths=('//div[@class="container"]//h4')),follow=True),
        Rule(LinkExtractor(allow=(r''),restrict_xpaths=('//div[@class="col-sm-6 content"]/table')), follow=False,callback='parse_item'),
    )

    def parse_item(self, response):
        item=HooliItem()
        Course = response.xpath('//section//h2//text()').extract()[0]
        long_str = response.xpath('//section[@class="sta-grey-light course"]//text()').extract()
        print(long_str,response.url)
        if 'UCAS code' in long_str:
            index_UCAS = long_str.index('UCAS code')
            CourseCode = long_str[index_UCAS + 1]
        else:
            CourseCode = ''
        Master = response.url.split('/')
        Master = Master[-2]
        Master = Master.split('-')
        Master = Master[-1].upper()

            # Duration
        if 'Course duration' in long_str:
            index_Duration = long_str.index('Course duration')
            Duration = long_str[index_Duration + 1]
        else:
            Duration = ''
        Career = response.xpath('//section[6]//text()').extract()
        Career = ''.join(Career).strip()

        long_str_date=''.join(long_str)
        # print(long_str_date)
        StartDate=re.findall('Start.+',long_str_date)
        if StartDate:
            StartDate=StartDate[0]
        else:
            StartDate=''
        Deadline = re.findall('End.+',long_str_date)
        if Deadline:
            Deadline=Deadline[0]
            # Alevel
        if 'GCE A-Levels' in long_str:
            index_Alevel = long_str.index('GCE A-Levels')
            Alevel = long_str[index_Alevel + 2]
        else:
            Alevel = ''
            # IB
        if 'IB points' in long_str:
            index_IB = long_str.index('IB points')
            IB = long_str[index_IB + 2]
        else:
            IB = ''
            # IELTS
        if 'International applicants' in long_str:
            index_IELTS = long_str.index('International applicants')
            IELTS = long_str[index_IELTS + 1:index_IELTS + 4]
            IELTS = ''.join(IELTS)
        else:
            IELTS = ''
        # CourseOverview
        CourseOverview = response.xpath('//section[2]//text()').extract()
        CourseOverview = ''.join(CourseOverview)
        # print(CourseOverview)
        # Assessment
        Assessment = response.xpath('//section[3]//text()').extract()
        Assessment = ''.join(Assessment).strip()
        # print(Assessment)
        # Modules
        Modules = response.xpath('//div[@id="year-tabs"]//text()').extract()
        Modules = ''.join(Modules).strip()
        # print(Modules)
        # TuitionFee
        Fee = response.xpath('//section[5]//text()').extract()
        if 'Overseas' in Fee:
            index_fee = Fee.index('Overseas')
            TuitionFee = Fee[index_fee + 2]
            TuitionFee = TuitionFee.replace(',', '')
            TuitionFee = TuitionFee.replace('£', '')
        else:
            TuitionFee = ''
        # if TuitionFee=='':
            # TuitionFee = re.findall('£\d+,\d+', long_str)
        # print(TuitionFee)
        # Career
        Career = response.xpath('//section[6]//text()').extract()
        Career = ''.join(Career).strip()
        EntryRequirements=''.join(long_str).strip()
        url = response.url
        University = 'St-Andrews'
        item["url"] = url
        item["University"] = University
        item["Course"] = Course
        item["CourseCode"] = CourseCode
        item["Master"] = Master
        item["CourseOverview"] = CourseOverview
        item["Alevel"] = Alevel
        item["IB"] = IB
        item["IELTS"] = IELTS
        item["TOEFL"] = ''
        item["Assessment"] = Assessment
        item["Career"] = Career
        item["TuitionFee"] = TuitionFee
        item["Modules"] = Modules
        item["Duration"] = Duration
        item["StartDate"] = StartDate
        item["Deadline"] = Deadline
        item["EntryRequirements"] = EntryRequirements
        item["Location"] = ''
        item["Department"] = ''

        yield item