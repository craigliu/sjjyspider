# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ApartmentItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    roomType = scrapy.Field()
    unitPrice = scrapy.Field()
    community = scrapy.Field()
    location = scrapy.Field()
    size = scrapy.Field()
    floor = scrapy.Field()
    decoration = scrapy.Field()
    description = scrapy.Field()

class CommunityItem(scrapy.Item):
    name = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    edge = scrapy.Field()
    apartNum = scrapy.Field()
    buildTime = scrapy.Field()
    location = scrapy.Field()
    developer = scrapy.Field()
    plotRate = scrapy.Field()
    propMgr = scrapy.Field()
    rentRate = scrapy.Field()
    parkingNum = scrapy.Field()
    greeningRate = scrapy.Field()
    description = scrapy.Field()

class OfficeItem(scrapy.Item):
    name = scrapy.Field()
    dailyPrice = scrapy.Field()
    dailyUnit = scrapy.Field()
    totalPrice = scrapy.Field()
    totalUnit = scrapy.Field()
    propMgFee = scrapy.Field()
    size = scrapy.Field()
    location = scrapy.Field()
    floor = scrapy.Field()
    type_ = scrapy.Field()
    buildTime = scrapy.Field()
    description = scrapy.Field()

class PoiBoundItem(scrapy.Item):
    name = scrapy.Field()
    bound = scrapy.Field()
    srcName = scrapy.Field()
    sim = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()

class BaiduItem(scrapy.Item):
    name = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()