import scrapy
from scrapy.selector import Selector


class CsgSpider(scrapy.Spider):
    name = 'csg'
    allowed_domains = ['www.bidding.csg.cn']
    start_urls = ['https://www.bidding.csg.cn/zbgg/index.jhtml']

    def parse(self, response):
        index_list = []
        for i in range(1, 2):
            index = 'https://www.bidding.csg.cn/zbgg/index_'+str(i)+'.jhtml'
            print(index)
            index_list.append(index)

        for index in index_list:
            yield scrapy.Request(url=index,callback=self.parse_index)
        # items = Selector(response=response).xpath('/html/body/section/div[3]/div[1]/ul/li')

    def parse_index(self, response):
        items = Selector(response=response).xpath('/html/body/section/div[3]/div[1]/ul/li')
        for item in items:
            bidding_company = item.xpath('./a[1]/text()').extract()[0]
            project_name = item.xpath('./a[2]/text()').extract()[0]
            bidding_type = item.xpath('./span[1]/a/text()').extract()[0]
            bidding_date = item.xpath('./span[1]/span/text()').extract()[0]
            bidding_url = 'https://www.bidding.csg.cn/'+item.xpath('./a[2]/@href').extract()[0]

            print('-----------------------')
            print(bidding_company)
            print(project_name)
            print(bidding_type)
            print(bidding_date)
            print(bidding_url)
            print('-----------------------')

            yield scrapy.Request(url=bidding_url,callback=self.parse_item)

    def parse_item(self, response):

        print(response.url)

        bidding_table = Selector(response=response).xpath('//table')
        # bidding_table_title = Selector(response=response).xpath('/html/body/section/div[2]/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/p/span[1]')
        print('-----------------------')

        print(bidding_table[0])

        print('-----------------------')

