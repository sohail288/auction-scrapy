# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

currency_re = re.compile(r'[^0-9.]')

class AuctionItem(scrapy.Item):

    url    = scrapy.Field()
    winner = scrapy.Field()
    price_sold = scrapy.Field()
    category   = scrapy.Field()
    name       = scrapy.Field()

    description = scrapy.Field()
    has_video = scrapy.Field()
    bid_history = scrapy.Field()
    number_photos = scrapy.Field()

    # calculate duration in pipeline
    bidding_start_date = scrapy.Field()
    bidding_end_date   = scrapy.Field()
    duration           = scrapy.Field()

   
    auction_name = scrapy.Field()    
    auction_description = scrapy.Field()
    auction_url = scrapy.Field()

    location = scrapy.Field()
    buyers_premium_amount = scrapy.Field()


