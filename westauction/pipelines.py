# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import AuctionItem
import re

currency_re = re.compile(r'[^0-9.]') 

def convertCurrency(currency_str):
    return re.sub(currency_re, '', currency_str)


class AuctionItemPipeline(object):
    
    def process_item(self, item, spider):
        if isinstance(item, AuctionItem):
            item['price_sold'] = convertCurrency(item['price_sold'])
        return item


    # need to convert the description to a suitable attributes/additional_information format
    # need to calculate duration of auction
    # need to make a list of bids
