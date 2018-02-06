# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
from myspider.items import HooliItem
class ArtsSpider(CrawlSpider):
    name = 'arts'
    allowed_domains = ['arts.ac.uk']
    #本科规则
    # start_urls = ['http://search.arts.ac.uk/s/search.html?collection=courses&query=&profile=_default&f.Course+level%7Cl=Undergraduate&f.Course+level%7Cl=Undergraduate&f.Mode%7Cm=Full+time&start_rank=1']
    # rules = (
    #     Rule(LinkExtractor(allow=r'start_rank=[0-9]+'),follow=True),
    #     Rule(LinkExtractor(allow=r'arts.ac.uk/[a-z-]+/'), follow=False,callback='parse_arts'),
    # )
    #研究生规则
    # start_urls = ['http://search.arts.ac.uk/s/search.html?collection=courses&query=&profile=_default&f.Course+level%7Cl=Postgraduate&f.Mode%7Cm=Full+time&start_rank=1']
    # rules = (
    #     Rule(LinkExtractor(allow=r'start_rank=[0-9]+'),follow=True),
    #     Rule(LinkExtractor(allow=r'arts.ac.uk/[a-z-]+/'), follow=False, callback='parse_arts_g'),
    # )
    def parse_arts(self, response):
        a=response.url
        a=a.split('/')
        if 'courses' in a:
            print('--------------------------',response.url)
            item = HooliItem()
            #学校 University of the Arts London
            University='University of the Arts London'

            #学院
            Department=response.xpath('//nav[@class="college"]//text()').extract()[0]

            #学位类型
            TypeOfDegree='undergraduate'

            url_long_str=response.xpath('//div[@class="ual-container"]//text()').extract()

            # 入学时间
            str_startdate='Start date'
            index_startdate=url_long_str.index(str_startdate)
            StartDate=url_long_str[index_startdate+1]

            #课程长度
            str_Duration='Course length'
            index_Duration=url_long_str.index(str_Duration)
            Duration=url_long_str[index_Duration+1]

            #CourseCode
            str_CourseCode='UCAS code'
            index_CourseCode=url_long_str.index(str_CourseCode)
            CourseCode=url_long_str[index_CourseCode+1]

            # #学位类型
            Master = response.url.split('/')
            Master = Master[-2]
            Master = Master.split('-')[0].upper()
            # print(Master)
            Course = response.url.split('/')[-2].upper()
            Course = Course.replace(Master, '')
            Course = Course.replace('-',' ').strip()
            #课程描述
            #//div[@id="tab1-panel"]//text()
            CourseOverview=response.xpath('//div[@id="tab1-panel"]//text()').extract()
            CourseOverview=''.join(CourseOverview)

            #课程设置
            Modules=response.xpath('//div[@id="tab2-panel"]//text()').extract()
            Modules=''.join(Modules)

            #申请要求
            EntryRequirements=response.xpath('//div[@id="tab3-panel"]//text()').extract()
            EntryRequirements=''.join(EntryRequirements)
            # print(EntryRequirements)
            IELTS=re.findall('IELTS[, \da-zA-Z.() ]{0,88}',EntryRequirements)
            IELTS=''.join(IELTS)
            url_long_str2=response.xpath('//div[@id="tab4-panel"]//text()').extract()
            # print(url_long_str2)
            # 学费
            str_TuitionFee = 'International fee'
            index_TuitionFee = url_long_str2.index(str_TuitionFee)
            TuitionFee = url_long_str2[index_TuitionFee + 1]
            TuitionFee = re.findall(r"£\d+,\d+", TuitionFee)[0]
            TuitionFee = TuitionFee.replace(',', '').replace('£', '')

            #就业方向
            Career=response.xpath('//div[@id="tab5-panel"]//text()').extract()
            Career=''.join(Career)

            item["url"] = response.url
            item["University"] = University
            item["Department"] = Department
            item["Location"] = ''
            item["Course"] = Course
            item["CourseCode"] = CourseCode
            item["Master"] = Master
            item["CourseOverview"] = CourseOverview
            item["Alevel"] = ''
            item["IB"] = ''
            item["IELTS"] = IELTS
            item["TOEFL"] = ''
            item["Assessment"] = ''
            item["Career"] = Career
            item["TuitionFee"] = TuitionFee
            item["Modules"] = Modules
            item["Duration"] = Duration
            item["StartDate"] = StartDate
            item["Deadline"] = ''
            item["EntryRequirements"] = EntryRequirements
            yield item


    def parse_arts_g(self, response):
        a=response.url
        a=a.split('/')
        if 'postgraduate' in a:
            print('--------------------------',response.url)
            item = HooliItem()
            #学校 University of the Arts London
            University='University of the Arts London'

            # #学院
            Department=response.xpath('//nav[@class="college"]//text()').extract()[0]

            # #学位类型
            Master=response.url.split('/')
            Master=Master[-2]
            Master=Master.split('-')[0].upper()
            # print(Master)
            Course =response.xpath('//h1/text()').extract()[0]
            Course=Course.replace(Master,'').strip()
            # print(Course)


            url_long_str=response.xpath('//div[@class="ual-container"]//text()').extract()

            # 入学时间
            str_startdate='Start date'
            index_startdate=url_long_str.index(str_startdate)
            StartDate=url_long_str[index_startdate+1]

            #课程长度
            str_Duration='Course length'
            index_Duration=url_long_str.index(str_Duration)
            Duration=url_long_str[index_Duration+1]

            # print(StartDate,Duration,response.url)

            #
            #课程描述
            #//div[@id="tab1-panel"]//text()
            CourseOverview=response.xpath('//div[@id="tab1-panel"]//text()').extract()
            CourseOverview=''.join(CourseOverview)
            #
            #课程设置
            Modules=response.xpath('//div[@id="tab2-panel"]//text()').extract()
            Modules=''.join(Modules)
            #
            #申请要求
            EntryRequirements=response.xpath('//div[@id="tab3-panel"]//text()').extract()
            EntryRequirements=''.join(EntryRequirements)
            #
            url_long_str2=response.xpath('//div[@id="tab4-panel"]//text()').extract()
            # print(url_long_str2)
            # 学费
            str_TuitionFee='International fee'
            index_TuitionFee=url_long_str2.index(str_TuitionFee)
            TuitionFee=url_long_str2[index_TuitionFee+1]
            TuitionFee=re.findall(r"£\d+,\d+",TuitionFee)[0]
            TuitionFee=TuitionFee.replace(',','').replace('£','')
            # print(TuitionFee)

            #就业方向
            Career=response.xpath('//div[@id="tab5-panel"]//text()').extract()
            Career=''.join(Career)

            Location=response.xpath('//div[@itemprop="address"]//text()').extract()
            Location=''.join(Location).strip()
            # print(Location)

            item["url"] = response.url
            item["University"] = University
            item["Location"] = Location
            item["Department"] = Department
            item["Course"] = Course
            item["CourseCode"] = ''
            item["Master"] = Master
            item["CourseOverview"] = ''
            item["Alevel"] = ''
            item["IB"] = ''
            item["IELTS"] = ''
            item["TOEFL"] = ''
            item["Assessment"] = ''
            item["Career"] = Career
            item["TuitionFee"] = TuitionFee
            item["Modules"] = Modules
            item["Duration"] = Duration
            item["StartDate"] = StartDate
            item["Deadline"] = ''
            item["EntryRequirements"] = EntryRequirements
            yield item