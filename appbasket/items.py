# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AppbasketItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    channel 		= scrapy.Field()
    crawl_time		= scrapy.Field()
    crawl_url		= scrapy.Field()
    name			= scrapy.Field()
    size 			= scrapy.Field()
    update_time 	= scrapy.Field()
    category		= scrapy.Field()
    tag				= scrapy.Field()
    version			= scrapy.Field()
    system			= scrapy.Field()
    source			= scrapy.Field()
    install_count	= scrapy.Field()
    like_count		= scrapy.Field()
    comment_count 	= scrapy.Field()
    comment_best_count	= scrapy.Field()
    comment_good_count	= scrapy.Field()
    comment_bad_count	= scrapy.Field()
    editor_comment	= scrapy.Field()
    desc_info		= scrapy.Field()
    score           = scrapy.Field()
    feature         = scrapy.Field()

