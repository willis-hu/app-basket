# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import codecs


class AppbasketPipeline(object):
	def __init__(self):
		self.file = codecs.open('wandoujia.json', mode='wb', encoding = 'utf-8')

	def process_item(self, item, spider):
		# json格式存储
		line = json.dumps(dict(item)) + '\n'
		self.file.write(line.decode("unicode_escape"))

		return item
