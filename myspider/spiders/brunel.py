# -*- coding: utf-8 -*-
import datetime
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider.items import HooliItem
import re

class BrunelSpider(CrawlSpider):
    name = 'brunel'
    allowed_domains = ['www.brunel.ac.uk']
    #本科爬取规则
    start_urls = ['http://www.brunel.ac.uk/study/Course-listing?courseLevel=0%2f2%2f24%2f28%2f43']

    rules = (
        Rule(LinkExtractor(allow=r'www.brunel.ac.uk/study/Course-listing\?courseLevel=0%2f2%2f24%2f28%2f43&page=[0-9]+'),follow=True),
        Rule(LinkExtractor(allow=r'www.brunel.ac.uk/study/undergraduate/.*'), follow=False, callback='parse_brunel'),
    )

    def parse_brunel(self, response):
        print('brunel----------------------------brunel',response.url)
        item=HooliItem()
        # 专业
        programme = response.xpath('//h1//text()').extract()[0]
        Master=response.url.split('/')[-1]
        Master=Master.split('-')[-1]
        # 专业描述
        overview = response.xpath('//div[@class="important_course_info"]//text()').extract()
        if overview == []:
            overview = 'null'
        else:
            overview = ''.join(overview).strip()

        url_long_right = response.xpath('//div[@class="featureBlock clearfix"]//text()').extract()
        # print(url_long_right)

        # 课程长度
        str_duration = 'Mode of study'
        index_duration = url_long_right.index(str_duration)
        Duration = url_long_right[index_duration + 2]
        # UCAS_code
        str_CAS_code = 'UCAS Code'
        index_UCAS_Code = url_long_right.index(str_CAS_code)
        UCAS_code = url_long_right[index_UCAS_Code + 2]
        # startdate 开始日期
        str_startdate = 'Start date'
        index_startdate = url_long_right.index(str_startdate)
        startdate = url_long_right[index_startdate + 2]
        # 课程设置
        modules = response.xpath('//article[@class="mainArticle"]/section[2]//text()').extract()
        if modules == []:
            modules = 'uncleared'
        else:
            long_str = '\n                  \n                \tRead more about the '
            if long_str in modules:
                index1 = modules.index(long_str)
                modules = modules[0:index1]
                modules = ''.join(modules)

        # 就业方向
        career = response.xpath('//article[@class="mainArticle"]/section[3]//text()').extract()
        if career == []:
            career = 'uncleared'
        else:
            long_str2 = '» More about Employability'
            if long_str2 in career:
                index2 = career.index(long_str2)
                career = career[0:index2]
                career = ''.join(career).strip()

        url_long_str = response.xpath('//article[@class="mainArticle"]/section[4]//text()').extract()
        long_str3 = 'Entry Criteria 2018/19'
        long_str4 = 'International and EU Entry Requirements'
        long_str5 = 'English Language Requirements'
        index_str3 = url_long_str.index(long_str3)
        index_str4 = url_long_str.index(long_str4)
        index_str5 = url_long_str.index(long_str5)
        # 申请要求
        Application_requirements = url_long_str[index_str3:index_str4]
        Application_requirements = ''.join(Application_requirements).strip()
        # 雅思
        IELTS = url_long_str[index_str5 + 3]
        IELTS = IELTS.replace('IELTS:', '').strip()

        # 评估方式
        url_long_str2 = response.xpath('//article[@class="mainArticle"]/section[5]//text()').extract()
        str_btt = 'Back to top'
        index_str6 = url_long_str2.index(str_btt)
        Evaluation_method = url_long_str2[1:index_str6]
        Evaluation_method = ''.join(Evaluation_method).strip()

        # 学费
        url_long_str3 = response.xpath('//article[@class="mainArticle"]/section[7]//text()').extract()
        str_IS = 'International students:'
        index_IS = url_long_str3.index(str_IS)
        tuition_fee = url_long_str3[index_IS + 2]
        tuition_fee = re.findall('\d+',tuition_fee)
        tuition_fee = ''.join(tuition_fee)
        # print(tuition_fee,response.url)

        item["university"] = 'Brunel University London'
        item["location"] = ''
        item["department"] = ''
        item["programme"] =programme
        item["ucas_code"] = UCAS_code
        item["degree_type"] = Master
        item["overview"] = overview
        item["IELTS"] = IELTS
        item["TOEFL"] = ''
        item["Alevel"] = ''
        item["IB"] = ''
        item["teaching_assessment"] = Evaluation_method
        item["career"] = career
        item["tuition_fee"] = tuition_fee
        item["modules"] = modules
        item["duration"] = Duration
        item["start_date"] = startdate
        item["deadline"] = ''
        item["entry_requirements"] = Application_requirements
        item["url"] = response.url
        yield item

    def parse_brunel_postgraduate(self,response):
        # print('11111111111111111')
        item=HooliItem()
        longstr=response.xpath('//div[@class="featureBlock clearfix"]//text()').extract()
        # print(longstr,response.url)
        if 'Mode of study' in longstr:
            index_Duration=longstr.index('Mode of study')
            Duration=longstr[index_Duration+2]
            Duration=''.join(Duration).strip()
            # print(Duration,response.url)
        else:
            Duration=''
        if 'Start date' in longstr:
            index_Duration=longstr.index('Start date')
            StartDate=longstr[index_Duration+2]
            StartDate=''.join(StartDate).strip()
            # print(StartDate,response.url)
        else:
            StartDate=''

        #专业名
        try:
            Course=response.url.split('/')[-1]
            Master=Course.split('-')[-1]
            Course=' '.join(Course.split('-'))
            Course=Course.replace(Master,'')
            # print(Course,Master,response.url)
        except:
            Course=''

        #雅思
        IELTS=response.xpath('//div[@class="featureBlock"]//li//text()').extract()[0]
        IELTS=IELTS.replace('IELTS:','')
        # print(IELTS,response.url)

        #学费
        try:
            TuitionFee=response.xpath('//div[@class="featureBlock"]/p/span/text()').extract()
            index_TuitionFee=TuitionFee.index('International students:')
            TuitionFee=TuitionFee[index_TuitionFee+1]
            TuitionFee=TuitionFee.replace(',','')
            TuitionFee=TuitionFee.replace('£','')
            # print(TuitionFee,response.url)
        except:
            TuitionFee=''
            print(response.url,'------------------------------------------')

        #//h4[@id="assessment"]/following-sibling::*
        #评估
        Assessment=response.xpath('//h4[@id="assessment"]/following-sibling::*//text()').extract()
        Assessment=''.join(Assessment).strip()
        # print(Assessment,response.url)

        #//h2[@id="entrycriteria"]/following-sibling::ul
        #入学要求
        EntryRequirements=response.xpath('//h2[@id="entrycriteria"]/following-sibling::ul//text()').extract()
        EntryRequirements=''.join(EntryRequirements).strip()
        # print(EntryRequirements,response.url)

        #课程设置
        Modules=response.xpath('//h2[@id="coursecontent"]/following-sibling::*//text()').extract()
        clear_str=Modules.index('Back to top')
        Modules=Modules[0:clear_str]
        Modules=''.join(Modules)
        # print(Modules,response.url)

        #专业描述
        #//h2[@id="overview"]/following-sibling::*//text()
        CourseOverview=response.xpath('//h2[@id="overview"]/following-sibling::*//text()').extract()
        clear_str_2=CourseOverview.index('Back to top')
        CourseOverview=CourseOverview[0:clear_str_2]
        CourseOverview=''.join(CourseOverview)

        item["university"] = 'Brunel University London'
        item["location"] = ''
        item["department"] = ''
        item["programme"] = Course
        item["ucas_code"] = ''
        item["degree_type"] = Master
        item["overview"] =CourseOverview
        item["IELTS"] = IELTS
        item["TOEFL"] = ''
        item["Alevel"] = ''
        item["IB"] = ''
        item["teaching_assessment"] = Assessment
        item["career"] = ''
        item["tuition_fee"] = TuitionFee
        item["modules"] =Modules
        item["duration"] = Duration
        item["start_date"] = StartDate
        item["deadline"] = ''
        item["entry_requirements"] = EntryRequirements
        item["url"] = response.url

        yield item