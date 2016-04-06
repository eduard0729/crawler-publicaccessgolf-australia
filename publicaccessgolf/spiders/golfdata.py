# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider             import BaseSpider
from scrapy.selector import Selector
from publicaccessgolf.items          import PublicaccessgolfItem
from scrapy.http            import Request
import re
from urlparse import urlparse
import time

class GolfdataSpider(BaseSpider):
    name = "golfdata"
    start_urls = ['http://publicaccessgolf.com.au/tag/gippsland-east/', 'http://publicaccessgolf.com.au/tag/gippsland-and-phillip-island/', 'http://publicaccessgolf.com.au/tag/goldfields/', 'http://publicaccessgolf.com.au/tag/great-ocean-road/','http://publicaccessgolf.com.au/tag/macedon-ranges/', 'http://publicaccessgolf.com.au/tag/melbourne/', 'http://publicaccessgolf.com.au/tag/mornington-and-bellarine-peninsula/', 'http://publicaccessgolf.com.au/tag/murray-outback/', 'http://publicaccessgolf.com.au/tag/the-grampians/', 'http://publicaccessgolf.com.au/tag/wine-and-high-country/', 'http://publicaccessgolf.com.au/tag/yarra-valley-and-dandenongs/']
    allowed_domains = ["publicaccessgolf.com.au"]

    def parse(self, response):
        links = response.xpath('//h3[@class="title"]/a/@href').extract()
        crawledLinks    = []
        region = response.xpath('//*[@id="breadcrumbs"]/span/span/span/a/span/text()').extract()
        #Pattern to check proper link
        linkPattern     = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
        for x in links:
            # If it is a proper link and is not checked yet, yield it to the Sp
            request = scrapy.Request(x, self.parse_hotel)
            request.meta['region'] = region
            yield request

    def parse_hotel(self, response):
        title  = response.xpath('//h1/span/text()').extract()
        description = response.xpath('//div[@class="single__content"]/p/text()').extract()
        phone  = response.xpath('//li[@class="single__phone"]/a/text()').extract()
        address  = response.xpath('//div[@itemprop="address"]/text()').extract()
        item = PublicaccessgolfItem()
        item["title"] = title
        item["description"] = description
        item["phone"] = phone
        item["address"] = address
        item["region"] = response.meta['region']
        yield item