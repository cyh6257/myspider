# -*- coding: utf-8 -*-
import scrapy

from myspider.items import HooliItem

class BaiduSpider(scrapy.Spider):
    name = 'Hud'
    allowed_domains = ['https://courses.hud.ac.uk']
    base_url= 'https://courses.hud.ac.uk%s'
    start_urls = []
    C = []
    for i in C:
        fullurl = base_url % i
        start_urls.append(fullurl)
        def parse(self, response):
            #print(response.url)

            item = HooliItem()
            #1.专业
            Course = response.xpath('//h1/text()').extract()[0]
            #print(Course)

            # 2开学时间
            StartDate = response.xpath('//div[@class = "col-xs-12 col-md-2 col-md-offset-1 border-left start"]/p/text()').extract()[0]
            #print(StartDate)


            #3.UCAS code
            CourseCode = response.xpath('/html/body/div[3]/div[2]/div/div[7]/p/text()').extract()[0]
            #print(CourseCode)

            #4 Duration课程长度
            Duration =  response.xpath('/html/body/div[3]/div[2]/div/div[3]/p/text()').extract()[0]
            #print(Duration)


            #5专业描述
            CourseOverview = response.xpath('//*[@id="about"]/div/div/div[2]/text()').extract()[0]
            #print(CourseOverview)

            #6索引
            url = 'https://courses.hud.ac.uk'
            #print(url)
            #7 大学名称
            University = 'Huddersfiel'
            #print(University)


            #8 Assessment  评估方式
            try:
                Assessment = response.xpath('//*[@id="detail"]/div/div/div[3]/p[1]/strong/text()').extract()[0]
                #print(Assessment)

            except:
                Assessment = 'N/A'
                #print(Assessment)
            # 9 Alevel
            try:
                Alevel = response.xpath('/html/body/div[3]/div[2]/div/div[5]/p/span[1]/text()').extract()[0]
                Alevel = 'A Level - ' + Alevel
                #print(Alevel)
            except:
                Alevel = 'N/A'
                #print(Alevel)


            # 10 IB
            try:
                IB = response.xpath('/html/body/div[3]/div[2]/div/div[5]/p[2]/span/text()').extract()[0]
                IB = 'BTEC - ' + IB
                #print(IB)
            except:
                IB = 'N/A'
                #print(IB)

            # 11 申请要求
            EntryRequirements = str("BTEC: " + IB+  "+"+ "Alevel: " + Alevel)
            #print(EntryRequirements)

            item["Course"] = Course
            item["StartDate"] = StartDate
            item["CourseCode"] = CourseCode
            item["Duration"] = Duration
            item["CourseOverview"] = CourseOverview
            item["University"] = University
            item["Assessment"] = Assessment
            item["Alevel"] = Alevel
            item["IB"] = IB
            item["EntryRequirements"] = EntryRequirements
            item["url"] = url

            yield item



