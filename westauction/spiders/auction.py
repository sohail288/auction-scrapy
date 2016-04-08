# -*- coding:utf-8 -*-

import scrapy
from westauction.items import AuctionItem
import re


ARCHIVE_PATH = 'home/archive'


class AuctionSpider(scrapy.Spider):

    name = 'auction'
   # allowed_domains = ['westauction.com']

    _start_urls = ['http://www.bidrl.com',
                   'http://www.thediffchico.com',
                   'http://www.westauction.com',
                   'http://www.northstateauctions.com',
    ]

    # get the allowed domains from the start urls
    allowed_domains = map(lambda url: url.split('www.')[-1], _start_urls)

    # these points contain the beef of the data.  
    # alternatively, you can also scrape all the auctions, present, and future
    # by modifying this line
    start_urls = [url+'/'+ARCHIVE_PATH for url in _start_urls[1:2]]



        
    def parse(self, response):
        counter = 0
        for aucbox in response.xpath('//div[@class="aucbox"]'):
            url = (aucbox
                .xpath('.//a[@class="auction_link"]/@href')
                .extract_first()
            )
            description = (aucbox
                .xpath('.//p[2]/text()')
                .extract_first()
            )

            meta_info = {
                'auction_url': url,
                'auction_description': description,
            }

            if '/item/' in url:
                request = scrapy.Request(url, callback=self.parse_auction_item)
            else:
                request = scrapy.Request(url, callback=self.parse_auction_pages)
                counter += 1

            request.meta['meta_info'] = meta_info
            yield request

            if counter > 2:
                break

        # follow the next pages
            
    def parse_auction_pages(self, response):
        max_option= (response
            .xpath('//*[@id="pager-top"]/option[last()]/@value')
            .extract()
        )
        max_option = int(max_option[0]) if max_option else 1


        for page_num in range(1, max_option+1):
            url = response.url + '/page/{}'.format(page_num)

            # bouncing the item with the auction description/url filled
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta['meta_info'] = response.meta['meta_info']
            yield request
        

    def parse_page(self, response):
        gallery = response.xpath('//div[@id="item-content"]/div[2]')
        page_items= gallery.xpath('//div[@itemprop="offers"]')
        for item in page_items:
            
            url  = item.xpath('*[@itemprop="url"][1]/@href').extract()[0]

            domain, suffix = re.findall(
                    '(?P<domain>.*?)(?P<suffix>\.\w+/)', response.url)[0]

            url = domain+suffix+url
            
            request = scrapy.Request(url, callback=self.parse_auction_item)
            request.meta['meta_info'] = response.meta['meta_info']
            yield request
            

    def parse_auction_item(self, response):
        auction_item = AuctionItem()

        itemprops = response.xpath('//*[@itemprop]')
        itemprop_xp = './/descendant-or-self::*[@itemprop="{}"]'
        
        auction_item['category'] = itemprops.xpath(
            itemprop_xp.format('category')+'/@content').extract_first()
    
        auction_item['url'] = (itemprops
            .xpath(itemprop_xp.format('url')+'/@content')
            .extract_first()
        )
        
        auction_item['bidding_start_date'] = (itemprops
            .xpath(itemprop_xp.format('availabilityStarts')+'/@content')
            .extract_first()
        )

        auction_item['bidding_end_date'] = (itemprops
            .xpath(itemprop_xp.format('availabilityEnds') + '/@content')
            .extract_first()
        )

        auction_item['name'] = (itemprops
            .xpath(itemprop_xp.format('name') + '/text()')
            .extract_first()
        )

        auction_item['location'] = {}
        auction_item['location']['region'] = (itemprops
            .xpath(itemprop_xp.format('addressRegion')+'/text()')
            .extract_first()
        )
        auction_item['location']['locality'] = (itemprops
            .xpath(itemprop_xp.format('addressLocality')+'/text()')
            .extract_first()
        )
        auction_item['location']['postal_code'] = (itemprops
            .xpath(itemprop_xp.format('postalCode')+'/text()')
            .extract_first()
        )

        
        
        info = (response
            .css('#lsidebar')
            .css('.spiffyfg')                                       
            .xpath('descendant-or-self::*[contains(text(), '
                    '"Auction Information")]')
            .xpath('./parent::*/following-sibling::div[1]/div')
        )
        auction_item['auction_name'] = (info.css('h2')
            .xpath('text()')
            .extract_first()
        )
        auction_item['buyers_premium_amount'] = (info
            .xpath('./*[contains(text(), "Premium")]/text()')
            .extract_first()
        )

        bid_history = response.css('#bid-history').css('table')
        auction_item['bid_history'] = bid_history.extract_first()
        high_bidder_row = bid_history.css('tr:nth-child(2)')
        auction_item['winner'] = (high_bidder_row
            .css('td:nth-child(3)')
            .xpath('text()')
            .extract_first()
        )
        auction_item['price_sold'] = (high_bidder_row
            .css('td:nth-child(2)')
            .xpath('text()').extract_first()
        )

    
        auction_item['has_video']   = (True if response.css('#videos').extract()                                            else False
        )
        auction_item['number_photos'] = len(response.css('#images > ul > li'))
        auction_item['description'] = (response
            .css('#description > ul > li')
            .xpath('text()').extract()
        )

        auction_description = response.meta['meta_info']['auction_description']
        auction_url         = response.meta['meta_info']['auction_url']
        auction_item['auction_description'] = auction_description
        auction_item['auction_url']         = auction_url

        yield auction_item
        
    
        

         

