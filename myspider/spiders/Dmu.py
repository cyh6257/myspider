# -*- coding: utf-8 -*-
from myspider.items import HooliItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re

class DmuSpider(CrawlSpider):
    name = 'Dmu'
    allowed_domains = ['www.dmu.ac.uk']
    # 爬取研究生
    # start_urls = ['http://www.dmu.ac.uk/study/courses/postgraduate-courses/']
    # 爬取本科
    start_urls = ['http://www.dmu.ac.uk/study/courses/undergraduate-courses/']

    rules = (
        #研究生爬取规则
        # Rule(LinkExtractor(allow=r'www.dmu.ac.uk/study/courses/postgraduate-courses/postgraduate-courses.aspx\?courselisting1_List_GoToPage=[0-9]*'),follow=True),
        # Rule(LinkExtractor(allow=r'/postgraduate-courses/[a-zA-Z\-]+\/[a-zA-Z\-]+.aspx'), callback='parse_Dmu',follow=False),
        #本科爬取规则
        Rule(LinkExtractor(allow=r'www.dmu.ac.uk/study/courses/undergraduate-courses/undergraduate-courses.aspx\?courselisting1_List_GoToPage=[0-9]*'),follow=True),
        Rule(LinkExtractor(allow=r'/undergraduate-courses/[a-zA-Z\-]+\/[a-zA-Z\-]+.aspx'), callback='parse_Dmu',follow=False),
    )

    def parse_Dmu(self, response):
        # print('-----------------------------------',response.url)

        item=HooliItem()

        Internationnal = response.xpath('//div[@data-kftab="2"]//text()').extract()
        # print(response.url)

        #专业
        Course=response.xpath('//div[@class="block__details block__details--overlay block__details--courseOverlay"]//h1[@class="block__details__title"]//text()').extract()[0]
        Course=Course.strip()
        Master=re.findall('[A-Z]{1}[A-Za-z]{1,3}\s?\([a-zA-Z]*\)',Course)
        Master=''.join(Master)
        Course=Course.replace(Master,'')
        if Master=='':
            Master=re.findall('MA|MSc',Course)
            Master=''.join(Master)
            print(Master,Course,response.url)
        else:
            Master=''
        #专业描述
        CourseOverview=response.xpath('//div[@class="block large-8 columns course-col2"]//text()').extract()
        CourseOverview=''.join(CourseOverview).strip()
        #学费
        self.var_fee = 'Fees and funding:'
        self.var_fee_2 = 'Fees and funding 2017/18'
        if self.var_fee in Internationnal:
            index_fee = response.xpath('//div[@data-kftab="2"]//text()').extract().index(self.var_fee)
            tuition_fee = Internationnal[index_fee + 1]
            TuitionFee = re.findall(r"£\d*,?\d*", tuition_fee)

        elif self.var_fee_2 in Internationnal:
            index_fee = response.xpath('//div[@data-kftab="2"]//text()').extract().index(self.var_fee_2)
            tuition_fee = Internationnal[index_fee + 1]
            TuitionFee = re.findall(r"£\d*,?\d*", tuition_fee)
        else:
            TuitionFee = ''
        if TuitionFee!=[]:
            TuitionFee=''.join(TuitionFee)
            TuitionFee=re.findall('\d+',TuitionFee)
            TuitionFee=''.join(TuitionFee)
        else:
            TuitionFee=''
        # print(TuitionFee,response.url)

        # 地点
        if 'Location:' in Internationnal:
            index_Location = response.xpath('//div[@data-kftab="2"]//text()').extract().index('Location:')
            Location = Internationnal[index_Location + 1]
        else:
            Location = 'The Gateway Leicester LE1 9BH '

        # UCAS课程代码
        self.var1 = 'UCAS course code:'
        if self.var1 in Internationnal:
            index_UCAS = response.xpath('//div[@data-kftab="2"]//text()').extract().index(self.var1)
            CourseCode = Internationnal[index_UCAS + 1]
        elif 'UCAS course codes:' in Internationnal:
            index_UCAS = response.xpath('//div[@data-kftab="2"]//text()').extract().index('UCAS course codes:')
            CourseCode = Internationnal[index_UCAS + 1]
        else:
            CourseCode = re.findall('[A-Z]{1}[A-Z0-9]{3}',''.join(Internationnal))
            CourseCode = ''.join(CourseCode)
            CourseCode = CourseCode.replace('UCAS','')

        # 课程长度
        if 'Duration:' in Internationnal:
            index_Tt = response.xpath('//div[@data-kftab="2"]//text()').extract().index('Duration:')
            Teaching_type = Internationnal[index_Tt + 1]
        else:
            Teaching_type = ''

        #IELTS \d?.\d? .*

        # 申请要求
        standard= response.xpath('//div[@class="row row--block course-section course-section--criteria"]//text()').extract()
        standard=' '.join(standard)
        # print(standard,response.url)
        IB=re.findall('International Baccalaureate:[.\w\s+]{0,50}',standard)
        IB=''.join(IB)

        IELTS=re.findall('IELTS (.*){0,3} \d+.\d+ .*',standard)
        IELTS=''.join(IELTS)

        Alevel=re.findall('Normally[0-9A-Z\(\s\),-:]*or',standard)
        Alevel=''.join(Alevel)


        # 课程及评估
        Evaluation_method=response.xpath('//div[@id="cycle-slideshow_course"]//text()').extract()
        Evaluation_method=' '.join(Evaluation_method)
        Evaluation_method=Evaluation_method.strip()

        #就业
        Career=response.xpath('//div[@class="row row--block course-section course-section--opps"]//text()').extract()
        Career=''.join(Career).strip()
        # print(Career)
        University = 'De Montfort'
        item["University"]=University
        # item["Course"]=Course
        # item["TypeOfDegree"]='undergraduate'
        # item["CourseOverview"]=CourseOverview
        # item["Duration"]=Teaching_type
        # item["CourseCode"]=CourseCode
        # item["Assessment"]=Evaluation_method
        # item["TuitionFee"]=TuitionFee
        # item["Location"]=Location
        # item["url"]=response.url
        # item["EntryRequirements"]=standard
        # item["Career"]=Career
        item["url"] = response.url
        item["University"] = University
        item["Course"] = Course
        item["CourseCode"] = CourseCode
        item["Master"] = Master
        item["CourseOverview"] = CourseOverview
        item["Alevel"] = Alevel
        item["IB"] = IB
        item["IELTS"] = IELTS
        item["TOEFL"] = ''
        item["Assessment"] = Evaluation_method
        item["Career"] = Career
        item["TuitionFee"] = TuitionFee
        item["Modules"] = Evaluation_method
        item["Duration"] = Teaching_type
        item["StartDate"] = ''
        item["Deadline"] = ''
        item["EntryRequirements"] = standard
        item["Location"] = Location
        item["Department"] = ''

        yield item
