import scrapy
from selenium import webdriver


class SgccSpider(scrapy.Spider):
    name = 'sgcc'
    allowed_domains = ['ecp.sgcc.com.cn']
    start_urls = ['https://ecp.sgcc.com.cn/ecp2.0/portal/#/list/list-spe/2018032600289606_1_2018032700291334']

    def __init__(self):
        self.driver = webdriver.PhantomJS()
    
    # def start_requests(self):
    #     return super().start_requests()

    def parse(self, response):
        print('---------------------------------------')
        print(response.text)
        print('---------------------------------------')
