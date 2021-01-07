# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiddingInfoNewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table = "info_list"
    bidding_company = scrapy.Field()
    project_name = scrapy.Field()
    bidding_type = scrapy.Field()
    bidding_date = scrapy.Field()
    bidding_url = scrapy.Field()

class BiddingInfoNewItemDetail(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table = "info_detail"
    bidding_table_titles_list = scrapy.Field()
    bidding_table_items_list = scrapy.Field()


