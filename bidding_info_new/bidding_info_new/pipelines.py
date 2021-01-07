# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import csv


class BiddingInfoNewPipeline:

    def process_item(self, item, spider):
        return item

# class BiddingInfoNewDetailPipeline:
#     def process_item(self, item, spider):
#         return item

# class MyProjectPipeline(object):
# # 保存为csv格式
# def __init__(self):
#     # 打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
#     self.f = open("myproject.csv","a",newline="")
#     # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
#     self.fieldnames = ["m_num","m_name","s_name","i_date","l_work","m_style","c_work"]
#     # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
#     self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
#     # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
#     self.writer.writeheader()

# def process_item(self, item, spider):
#     # 写入spider传过来的具体数值
#     self.writer.writerow(item)
#     # 写入完返回
#     return item

# def close(self,spider):
#     self.f.close()








class MysqlPipeline(object):
    def __init__(self,host,user,password,database,port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get("MYSQL_HOST"),
            user = crawler.settings.get("MYSQL_USER"),
            password = crawler.settings.get("MYSQL_PASS"),
            database = crawler.settings.get("MYSQL_DATABASE"),
            port = crawler.settings.get("MYSQL_PORT"),
        )

    def open_spider(self, spider):
        '''负责连接数据库'''
        self.db = pymysql.connect(self.host,self.user,self.password,self.database,charset="utf8mb4",port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        '''执行数据表的写入操作'''
        #组装sql语句
        data = dict(item)
        keys = ','.join(data.keys())
        values=','.join(['%s']*len(data))
        sql = "insert into %s(%s) values(%s)"%(item.table,keys,values)
        #指定参数，并执行sql添加
        self.cursor.execute(sql,tuple(data.values()))
        #事务提交
        self.db.commit()
        return item

    def close_spider(self, spider):
        '''关闭连接数据库'''
        self.db.close()