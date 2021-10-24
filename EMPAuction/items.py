# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EmpauctionItem(scrapy.Item):
    title = scrapy.field()
    price = scrapy.field()
    high_bidder = scrapy.field()

    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
