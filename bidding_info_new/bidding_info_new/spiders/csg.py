import scrapy
from scrapy.selector import Selector
from bidding_info_new.items import BiddingInfoNewItem, BiddingInfoNewItemDetail
import re

class CsgSpider(scrapy.Spider):
    name = 'csg'
    allowed_domains = ['www.bidding.csg.cn']
    start_urls = ['https://www.bidding.csg.cn/zbgg/index.jhtml']

    def parse(self, response):
        index_list = []
        for i in range(1, 611):
            index = 'https://www.bidding.csg.cn/zbgg/index_'+str(i)+'.jhtml'
            print(index)
            index_list.append(index)

        for index in index_list:
            yield scrapy.Request(url=index,callback=self.parse_index)
        # items = Selector(response=response).xpath('/html/body/section/div[3]/div[1]/ul/li')

    def parse_index(self, response):
        

        items = Selector(response=response).xpath('/html/body/section/div[3]/div[1]/ul/li')
        for item in items:

            BiddingInfo = BiddingInfoNewItem()

            bidding_company = item.xpath('./a[1]/text()').extract()[0]
            project_name = item.xpath('./a[2]/text()').extract()[0]
            bidding_type = item.xpath('./span[1]/a/text()').extract()[0]
            bidding_date = item.xpath('./span[1]/span/text()').extract()[0]
            bidding_url = 'https://www.bidding.csg.cn/'+item.xpath('./a[2]/@href').extract()[0]

            BiddingInfo['bidding_company'] = bidding_company
            BiddingInfo['project_name'] = project_name
            BiddingInfo['bidding_type'] = bidding_type
            BiddingInfo['bidding_date'] = bidding_date
            BiddingInfo['bidding_url'] = bidding_url
            

            print('-----------------------')
            print(bidding_company)
            print(project_name)
            print(bidding_type)
            print(bidding_date)
            print(bidding_url)
            print('-----------------------')

            yield scrapy.Request(url=bidding_url,callback=self.parse_item)

            yield BiddingInfo

    def parse_item(self, response):

        BiddingInfoDetail = BiddingInfoNewItemDetail()
        
        bidding_table_titles_list = []
        bidding_table_items_list = []

        bidding_table_titles_list.append('网页链接')
        bidding_table_items_list.append(response.url)

        print(response.url)
        try:
            bidding_id_search = re.search(r'[0]{3}[0-9]{13}',response.text)

            if bidding_id_search:
                print(bidding_id_search.group())
                bidding_table_titles_list.append('项目编号')
                bidding_table_items_list.append(bidding_id_search.group())
            else:
                print('没有项目编号')
                bidding_table_titles_list.append('项目编号')
                bidding_table_items_list.append('没有项目编号')

            bidding_table = Selector(response=response).xpath('//table')[0]
            bidding_table_titles = bidding_table.xpath('.//tr[1]/td')
            bidding_table_items = bidding_table.xpath('.//tr[2]/td')

            print('-----------------------')
            for title in bidding_table_titles:
                # print(title.extract())
                span_sum = ''
                spans = title.xpath('.//span/text()')
                if len(spans) > 0:
                    for span_item in spans:
                        span_sum = span_sum+span_item.extract()

                ass_sum = ''
                aas = title.xpath('.//span/a/text()')
                if len(aas) > 0:
                    for ass_item in aas:
                        ass_sum = ass_sum+ass_item.extract()

                bidding_table_titles_list.append(span_sum+ass_sum)
            
            for item in bidding_table_items:
                
                span_sum = ''
                spans = item.xpath('.//span/text()')
                if len(spans) > 0:
                    for span_item in spans:
                        span_sum = span_sum+span_item.extract()

                ass_sum = ''
                aas = item.xpath('.//span/a/text()')
                if len(aas) > 0:
                    for ass_item in aas:
                        ass_sum = ass_sum+ass_item.extract()

                bidding_table_items_list.append(span_sum+ass_sum)

            print(bidding_table_titles_list)
            print(bidding_table_items_list)

            print('-----------------------')

            BiddingInfoDetail['bidding_table_titles_list'] = "|".join(bidding_table_titles_list)
            BiddingInfoDetail['bidding_table_items_list'] = "|".join(bidding_table_items_list)

            yield BiddingInfoDetail

        except IndexError:
            print('没有表格')
        
        # bidding_table_title = Selector(response=response).xpath('/html/body/section/div[2]/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/p/span[1]')

