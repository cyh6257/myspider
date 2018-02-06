# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider.items import HooliItem
from w3lib.html import remove_tags
import requests
class TextSpider(CrawlSpider):
    name = 'text'
    allowed_domains = ['www.harper-adams.ac.uk']
    start_urls = []
    base_url='https://www.harper-adams.ac.uk/courses/courses.cfm?q=&type=undergraduate&area=&yoe=2018&title=%s'
    Title=['A','B','C','F','G','M','P','R','V','W','Z']
    for i in Title:
        fullurl=base_url % i
        start_urls.append(fullurl)
        rules =(
            Rule(LinkExtractor(allow='.*'),follow=False,callback='parse_item'),
        )
    def parse_item(self, response):
        print('-------------------',response.url)
        urlid=response.url.split('/')[5]
        url_a='https://www.harper-adams.ac.uk/courses/undergraduate/get-entry-requirements.cfm?id=%s&qualification=alevels&year_of_entry=2018'
        url_a=url_a % urlid
        Alevels=requests.get(url_a)
        Alevels=Alevels.text
        Alevels=remove_tags(Alevels).strip()
        url_b='https://www.harper-adams.ac.uk/courses/undergraduate/get-entry-requirements.cfm?id=%s&qualification=IB&year_of_entry=2018'
        url_b=url_b % urlid
        IB=requests.get(url_b)
        IB=IB.text
        IB=remove_tags(IB).strip()
        item = HooliItem()
        url_lont_str = response.xpath('//div[@class="content-section-inner"]//text()').extract()
        # 专业名称
        Master = response.xpath('//div[@id="course-title"]//text()').extract()[0]
        Course = response.xpath('//div[@class="page-heading"]/h1//text()').extract()[0]
        # CourseCode
        index_UCAScode = url_lont_str.index('UCAS code')
        CourseCode = url_lont_str[index_UCAScode + 2]
        # 课程长度
        index_Duration = url_lont_str.index('Duration')
        Duration = url_lont_str[index_Duration + 2]
        # 开学时间
        index_Startdate = url_lont_str.index('Start date')
        StartDate = url_lont_str[index_Startdate + 2]
        # 地点
        index_Location = url_lont_str.index('Location')
        Location = url_lont_str[index_Location + 2]
        if 'Typical offer' in url_lont_str:
            index_Typicaloffer = url_lont_str.index('Typical offer')
            Typicaloffer = url_lont_str[index_Typicaloffer + 2]
        else:
            Typicaloffer = ''
        str_url_kcyq = response.xpath('//div[@id="overview"]//div[@class="content-section-inner"]//text()').extract()
        # 专业描述
        index_biaoji = str_url_kcyq.index('How to apply')
        CourseOverview = str_url_kcyq[0:index_biaoji - 2]
        sx = response.xpath('//div[@id="placement"]//div[@class="content-section-inner"]//text()').extract()
        CourseOverview = CourseOverview + sx
        CourseOverview = ''.join(CourseOverview).strip()
        # 评估方式
        Assessment = response.xpath('//div[@id="teaching"]//div[@class="content-section-inner"]//text()').extract()
        Assessment = ''.join(Assessment).strip()
        # 就业
        Career = response.xpath('//div[@id="careers"]//text()').extract()
        Career = ''.join(Career).strip()
        # 学费
        # 10400
        # 雅思
        IELTS = '6.0 (minimum 5.5 in any component)'
        # 托福
        TOEFL = '80+ (minimum 18 reading, 18 Listening, 22 speaking, 20 writing)'
        university = 'Harper Adams'

        item["university"] = university
        item["location"] = Location
        item["department"] = ''
        item["programme"] =Course
        item["ucas_code"] = CourseCode
        item["degree_type"] = Master
        item["overview"] = CourseOverview
        item["IELTS"] = IELTS
        item["TOEFL"] = TOEFL
        item["Alevel"] =Alevels
        item["IB"] = IB
        item["teaching_assessment"] = Assessment
        item["career"] = Career
        item["tuition_fee"] = '10400'
        item["modules"] = ''
        item["duration"] = Duration
        item["start_date"] = StartDate
        item["deadline"] = ''
        item["entry_requirements"] = Typicaloffer
        item["url"] = response.url
        item["Justone"] = response.url
        # yield item
        print(item)