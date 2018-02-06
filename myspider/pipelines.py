# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class MyspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlDB(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect('127.0.0.1','root','123456','hooli',charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('连接数据库失败：%s'% str(e))

    def close(self):
        self.cursor.close()
        self.conn.close()


# class Dmu(MysqlDB):
#     def process_item(self,item,spider):
#         sql='insert into school_gs(University,Course,TypeOfDegree,CourseOverview,Duration,CourseCode,Assessment,TuitionFee,Location,EntryRequirements,Career,url)'\
#             'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update Course = values(Course),TuitionFee= VALUES (TuitionFee),CourseOverview=VALUES (CourseOverview),' \
#             'EntryRequirements=VALUES (EntryRequirements),Career=VALUES (Career),Duration=VALUES (Duration),CourseCode=VALUES (CourseCode),TuitionFee=VALUES (TuitionFee),Assessment=VALUES (Assessment)'
#         try:
#             self.cursor.execute(sql,(
#                 item["University"],item["Course"],item["TypeOfDegree"],item["CourseOverview"],item["Duration"],item["CourseCode"],item["Assessment"],item["TuitionFee"],item["Location"],item["EntryRequirements"],item["Career"],item["url"]
#             ))
#             self.conn.commit()
#         except Exception as e:
#             self.conn.rollback()
#             print(e)
#             print("执行sql语句失败")
#         return item
#
# class Arts(MysqlDB):
#     def process_item(self,item,spider):
#         sql='insert into school_gs(University,Department,TypeOfDegree,Course,CourseCode,StartDate,Duration,Modules,EntryRequirements,TuitionFee,Career,url)'\
#             'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update Course = values(Course),EntryRequirements = values(EntryRequirements),TuitionFee= VALUES (TuitionFee),StartDate=VALUES (StartDate)'
#         try:
#             self.cursor.execute(sql,(
#                 item["University"],item["Department"],item["TypeOfDegree"],item["Course"],item["CourseCode"],item["StartDate"],item["Duration"],item["Modules"],item["EntryRequirements"],item["TuitionFee"],item["Career"],item["url"]
#             ))
#             self.conn.commit()
#         except Exception as e:
#             self.conn.rollback()
#             print(e)
#             print("执行sql语句失败")
#
#         return item
#
# class HarperAdams(MysqlDB):
#     def process_item(self,item,spider):
#         sql='insert into school_gs(University,Location,TypeOfDegree,Course,CourseOverview,CourseCode,StartDate,Duration,Assessment,Career,TuitionFee,IELTS,TOEFL,url,Alevel,IB)'\
#             'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update Course = values(Course),TuitionFee= VALUES (TuitionFee),StartDate=VALUES (StartDate)'
#         try:
#             self.cursor.execute(sql,(
#                 item["University"],item["Location"],item["TypeOfDegree"],item["Course"],item["CourseOverview"],item["CourseCode"],item["StartDate"],item["Duration"],item["Assessment"],item["Career"],item["TuitionFee"],item["IELTS"],item["TOEFL"],item["url"],item["Alevel"],item["IB"]
#             ))
#             self.conn.commit()
#         except Exception as e:
#             self.conn.rollback()
#             print(e)
#             print("执行sql语句失败")
#         return item
#
# class Southampton(MysqlDB):
#     def process_item(self,item,spider):
#         sql='insert into school_gs(University,Course,CourseCode,TypeOfDegree,CourseOverview,other,Alevel,IB,Assessment,Career,url)'\
#             'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update Course = values(Course),CourseCode=VALUES (CourseCode)'
#         try:
#             self.cursor.execute(sql,(
#                 item["University"],item["Course"],item["CourseCode"],item["TypeOfDegree"],item["CourseOverview"],item["other"],item["Alevel"],item["IB"],item["Assessment"],item["Career"],item["url"]
#             ))
#             self.conn.commit()
#         except Exception as e:
#             self.conn.rollback()
#             print(e)
#             print("执行sql语句失败")
#
#         return item
#
# class Hud(MysqlDB):
#     def process_item(self,item,spider):
#         sql='insert into school_gs(Course,StartDate,CourseCode,Duration,CourseOverview,University,Assessment,Alevel,IB,EntryRequirements)'\
#             'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#         try:
#             self.cursor.execute(sql,(
#                 item["Course"],item["StartDate"],item["CourseCode"],item["Duration"],item["CourseOverview"],item["University"],item["Assessment"],item["Alevel"],item["IB"],item["EntryRequirements"]
#             ))
#             self.conn.commit()
#         except Exception as e:
#             self.conn.rollback()
#             print(e)
#             print("执行sql语句失败")
#
#         return item
#
# class brunel(MysqlDB):
#     def process_item(self,item,spider):
#         sql='insert into school_gs(University,Course,TypeOfDegree,CourseOverview,Duration,CourseCode,StartDate,Assessment,TuitionFee,IELTS,Modules,EntryRequirements,Career,url,crawltime)'\
#             'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update TuitionFee = values(TuitionFee),Duration= VALUES (Duration),CourseCode=VALUES (CourseCode),StartDate=VALUES (StartDate),crawltime=VALUES (crawltime)'
#         try:
#             self.cursor.execute(sql,(
#                 item["University"],item["Course"],item["TypeOfDegree"],item["CourseOverview"],item["Duration"],item["CourseCode"],item["StartDate"],item["Assessment"],item["TuitionFee"],item["IELTS"],item["Modules"],item["EntryRequirements"],item["Career"],item["url"],item["crawltime"]
#             ))
#             self.conn.commit()
#         except Exception as e:
#             self.conn.rollback()
#             print(e)F100 BSc Chemistry  (3 years)
#             print("执行sql语句失败")
#
#         return item


class Hooli(MysqlDB):
    def process_item(self, item, spider):
        sql = 'insert into hooli(university,location,department,programme,ucas_code,degree_type,overview,Alevel,IB,IELTS,TOEFL,teaching_assessment,career,tuition_fee,modules,duration,start_date,deadline,entry_requirements,url,Justone)' \
              'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update department = values(department),modules= values(modules),entry_requirements = values(entry_requirements),' \
              'location = values(location),programme = values(programme),teaching_assessment = values(teaching_assessment),degree_type = values(degree_type),tuition_fee = values(tuition_fee),duration= VALUES (duration),ucas_code=VALUES (ucas_code),' \
              'start_date=VALUES (start_date),IELTS=VALUES (IELTS),TOEFL = values(TOEFL)'
        try:
            self.cursor.execute(sql, (
                item["university"],item["location"],item["department"], item["programme"], item["ucas_code"], item["degree_type"], item["overview"],
                item["Alevel"], item["IB"], item["IELTS"],item["TOEFL"], item["teaching_assessment"], item["career"],
                item["tuition_fee"], item["modules"], item["duration"], item["start_date"], item["deadline"], item["entry_requirements"], item["url"],item["Justone"]
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
            print("执行sql语句失败")

        return item
