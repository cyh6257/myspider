# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
from myspider.items import HooliItem

class YorkSpider(CrawlSpider):
    name = 'York'
    allowed_domains = ['www.york.ac.uk']
    start_urls = ['https://www.york.ac.uk/study/undergraduate/courses/all']

    # rules = (
    #     Rule(LinkExtractor(allow=r'www.york.ac.uk/study/undergraduate/courses/.*'), follow=False,callback='parse_item'),
    #     Rule(LinkExtractor(allow=r'www.york.ac.uk/[a-z]+/undergraduate/courses/.*'), follow=False,callback='parse_item_2'),
    # )
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@id="results"]/table/tbody/tr//a'), follow=False,callback='parse_text'),
    )

    def parse_text(self, response):
        urls=response.url.split('/')
        if 'study' in urls:
            item = HooliItem()
            url_text = response.xpath('//div[@class="o-grid__box o-grid__box--twothirds"]//text()').extract()
            url_text_2 = response.xpath('//div[@class="o-grid__box o-grid__box--full"]//ul//text()').extract()
            # 雅思
            if 'IELTS:' in url_text_2:
                index_IELTS = url_text_2.index('IELTS:')
                IELTS = url_text_2[index_IELTS + 1]
            else:
                IELTS = ''
            # 托福
            if 'TOEFL' in url_text_2:
                index_TOEFL = url_text_2.index('TOEFL')
                TOEFL = url_text_2[index_TOEFL + 1].replace(':', '')
            else:
                TOEFL = ''
            # 学院
            if 'Department' in url_text:
                index_Dep = url_text.index('Department')
                Department = url_text[index_Dep + 1]
            else:
                Department = ''
            # 专业名
            Course = response.xpath(
                '//div[@class="c-figure__content c-figure__content--left c-figure__content--half"]/h1//text()').extract()[0]
            Master = re.findall('[A-Za-z]{2,10}\s\([a-zA-Z]*\)', Course)
            if Master == []:
                Master = ''
            else:
                Master = ''.join(Master)
            Course = Course.replace(Master, '')
            # 入学时间
            self.startime = 'Start date'
            if self.startime in url_text:
                index_startime = url_text.index(self.startime) + 1
                StartDate = url_text[index_startime].replace('(', '')
            else:
                StartDate = ''
            # 专业描述
            overview = response.xpath(
                '//div[@class="o-grid__box o-grid__box--half o-grid__box--half@medium"]//text()').extract()
            CourseOverview = ''.join(overview).strip()
            # 课程长度
            if 'Length' in url_text:
                index_TT = url_text.index('Length') + 1
                Duration = url_text[index_TT]
            else:
                Duration = ''
            self.kcsz = 'UCAS code'
            if self.kcsz in url_text:
                index_kesz = url_text.index(self.kcsz)
                ucas_code = url_text[index_kesz + 1]
            else:
                ucas_code = ''

            Evaluation_method = response.xpath(
                '//div[@class="o-grid__box o-grid__box--half o-grid__box--half@medium o-grid__box--full@small"]//text()').extract()
            Assessment = ''.join(Evaluation_method).strip()

            long_str_eq = response.xpath('//div[@id="entry"]//text()').extract()
            if 'A levels' in long_str_eq:
                index_al = long_str_eq.index('A levels')
                Alevel = long_str_eq[index_al + 2]
            if 'International Baccalaureate' in long_str_eq:
                index_IB = long_str_eq.index('International Baccalaureate')
                IB = long_str_eq[index_IB + 2]
            else:
                IB = ''

            self.t_fee = 'International fees'
            if self.t_fee in url_text:
                index_tfee = url_text.index(self.t_fee)
                tuition_fee = url_text[index_tfee + 2]
                TuitionFee = re.findall('\d+,\d+', tuition_fee)[0]
                TuitionFee = TuitionFee.replace(',', '')
            else:
                TuitionFee = ''

            University = 'University of York'

            item["university"] = University
            item["location"] = ''
            item["department"] = Department
            item["programme"] = Course
            item["ucas_code"] = ucas_code
            item["degree_type"] = Master
            item["overview"] = CourseOverview
            item["IELTS"] = IELTS
            item["TOEFL"] = TOEFL
            item["Alevel"] = Alevel
            item["IB"] =IB
            item["teaching_assessment"] = Assessment
            item["career"] = ''
            item["tuition_fee"] = TuitionFee
            item["modules"] = ''
            item["duration"] = Duration
            item["start_date"] = StartDate
            item["deadline"] = ''
            item["entry_requirements"] = ''
            item["url"] = response.url
            yield item
        else:
            item = HooliItem()
            url_text = response.xpath('//table[@id="course-summary-table"]//text()').extract()
            index_ucas = url_text.index('UCAS\xa0code')
            ucas_code = url_text[index_ucas + 8]
            Duration = url_text[index_ucas + 15]
            overview = response.xpath('//div[@id="course-overview-content"]//text()').extract()
            CourseOverview = ''.join(overview).strip()
            modules = response.xpath('//div[@id="course-content-content"]//text()').extract()
            Modules = ''.join(modules).strip()
            Evaluation_method = response.xpath('//div[@id="course-assessment-content"]//text()').extract()
            Assessment = ''.join(Evaluation_method).strip()
            TuitionFee = ''
            Course = response.xpath('//*[@id="course-summary"]//text()').extract()[1]
            Master=re.findall('[A-Za-z]{2,10}\s\([a-zA-Z]*\)',Course)
            if Master==[]:
                Master=''
            else:
                Master=''.join(Master)
            Course=Course.replace(Master,'')
            Career = response.xpath('//*[@id="course-careers-content"]//text()').extract()
            Career = ''.join(Career).strip()
            University = 'University of York'


            item["university"] =University
            item["location"] = ''
            item["department"] = ''
            item["programme"] =Course
            item["ucas_code"] = ucas_code
            item["degree_type"] = Master
            item["overview"] = CourseOverview
            item["IELTS"] = 'IELTS 6.5'
            item["TOEFL"] = ''
            item["Alevel"] = ''
            item["IB"] =''
            item["teaching_assessment"] = Assessment
            item["career"] = Career
            item["tuition_fee"] = TuitionFee
            item["modules"] = Modules
            item["duration"] = Duration
            item["start_date"] = ''
            item["deadline"] = ''
            item["entry_requirements"] = ''
            item["url"] = response.url

            yield item

