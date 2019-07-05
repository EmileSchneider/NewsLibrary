# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewslibItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    punchword = scrapy.Field()
    category = scrapy.Field()
    headline = scrapy.Field()
    subline = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
