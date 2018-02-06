# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider.items import HooliItem
import re

class SouthamptonSpider(CrawlSpider):
    name = 'Southampton'
    allowed_domains = ['www.southampton.ac.uk']
    #本科抓取规则
    start_urls = ['https://www.southampton.ac.uk/courses/undergraduate.page']
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="uos-all-course-groups"]/dl/dd/a'),follow=False,callback='parse_Southampton'),
    )
    def parse_Southampton(self, response):
        if True:
            # print(response.url,'------------------------------------------------')
            item=HooliItem()
            #专业
            Course=response.xpath('//h1[@class="uos-page-title uos-main-title"]//text()').extract()
            Course=''.join(Course)

            #UCAS
            CourseCode=response.xpath('//aside//text()').extract()[4]
            #学位类型
            TypeOfDegree=response.xpath('//aside//text()').extract()[6]

            #专业描述
            #//div[@class="uos-page-intro"]//text() 专业描述第一部分
            #//div[@class="uos-grid uos-grid-2-3"]//text() 第二
            part1=response.xpath('//div[@class="uos-page-intro"]//text() ').extract()
            part2=response.xpath('//div[@class="uos-grid uos-grid-2-3"]//text()').extract()
            part3 = response.xpath('//div[@data-target="tabset-1"]//text()').extract()
            CourseOverview=part1+part2+part3
            CourseOverview=''.join(CourseOverview).strip()

            #学术要求
            xsyq=response.xpath('//div[@data-target="tabset-2"]//text()').extract()
            # print(xsyq,response.url)

            if 'GCSE' in xsyq:
                index_GCSE=xsyq.index('GCSE')
                GCSE=xsyq[index_GCSE+1]
                # print(GCSE)
            else:
                GCSE=''
            #Aleve
            if 'GCE A-level' in xsyq:
                index_Aleve=xsyq.index('GCE A-level')
                Aleve=xsyq[index_Aleve+1]
                Aleve=Aleve+GCSE
                # print(Aleve,response.url)
            else:
                Aleve='uncleared'


            #IB
            if 'International Baccalaureate'in xsyq:
                index_InternationalBaccalaureate=xsyq.index('International Baccalaureate')
                IB=xsyq[index_InternationalBaccalaureate+1]
                # print(IB,response.url)
            else:
                IB='uncleared'

            #用来区分有无评估标签
            len_div=response.xpath('//div[@id="js-component-tabs"]/h3/text()').extract()
            len_div=len(len_div)
            # 评估
            if len_div>=6:
                Assessment = response.xpath('//div[@data-target="tabset-6"]//text()').extract()
                Assessment=''.join(Assessment)
                # print(Assessment,response.url)
            else:
                Assessment='uncleared'

            #课程要求
            Modules=response.xpath('//div[@data-target="tabset-3"]//text()').extract()
            Modules=''.join(Modules)
            # print(Modules)

            #就业
            Career=response.xpath('//div[@data-target="tabset-5"]//text()').extract()
            Career=''.join(Career)

            #学费
            TuitionFee=response.xpath('//table[@class="uos-table"]//text()').extract()
            if TuitionFee!=[]:
                if 'Full-time' in TuitionFee:
                    index_fee=TuitionFee.index('Full-time')+2
                    TuitionFee=TuitionFee[index_fee]
                    TuitionFee=TuitionFee.replace(',','').replace('£','')
                else:
                    TuitionFee=''
            else:
                TuitionFee=''
            EntryRequirements=response.xpath('//div[@data-target="tabset-2"]//text()').extract()
            EntryRequirements=''.join(EntryRequirements)

            University='Southampton'
            # other=''.join(xsyq).strip()
            Duration=re.findall('\(\d.*\)',Course)
            Duration=''.join(Duration)
            Course=Course.replace(Duration,'').replace(CourseCode,'').strip()
            # print(Duration,Course,response.url)
            item["university"] = University
            item["location"] = ''
            item["department"] = ''
            item["ucas_code"] = CourseCode
            item["programme"] = Course
            item["degree_type"] = TypeOfDegree
            item["overview"] = CourseOverview
            item["IELTS"] = ''
            item["TOEFL"] = ''
            item["Alevel"] = Aleve
            item["IB"] = IB
            item["teaching_assessment"] = Assessment
            item["career"] = Career
            item["tuition_fee"] = TuitionFee
            item["modules"] = Modules
            item["duration"] =Duration
            item["start_date"] =''
            item["deadline"] = ''
            item["entry_requirements"] = EntryRequirements
            item["url"] = response.url
            yield item

