# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EntityItem(scrapy.Item):
    id_ = scrapy.Field()
    brand = scrapy.Field()
    type_ = scrapy.Field()
    year = scrapy.Field()
    version_ = scrapy.Field()
class FontItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
class ClassItem(scrapy.Item):
    id_ = scrapy.Field()
    name = scrapy.Field()

