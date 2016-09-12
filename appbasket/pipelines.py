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
from scrapy.exceptions import DropItem

class AppbasketPipeline(object):
	def __init__(self):
		self.file = codecs.open('data/app-data.tsv', mode='wb', encoding = 'utf-8')
		self.urls = set()

	def process_item(self, item, spider):
		# item去重
		if item['crawl_url'] in self.urls:
			raise DropItem("Duplicate item found: %s" % item['crawl_url'])
		self.urls.add(item['crawl_url'])

		# item为空检查
		if "NULL" == item['name']:
			raise DropItem("Empty item found: %s" % item['crawl_url'])

		# json格式存储
		# line = json.dumps(dict(item)) + '\n'
		# self.file.write(line.decode("unicode_escape"))

		# tsv格式存储
		line =  "%s\t%d\t%s\t%s\t%d\t%d\t%s\t%s\t%s\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%s\t%s\t%d\t%s\n" % ( 		\
			item['channel'], 		\
			item['crawl_time'], 	\
			item['crawl_url'], 		\
			item['name'], 			\
			item['size'], 			\
			item['update_time'], 	\
			item['category'], 		\
			item['tag'], 			\
			item['version'], 		\
			item['system'], 		\
			item['source'], 		\
			item['install_count'], 	\
			item['like_count'], 	\
			item['comment_count'], 	\
			item['comment_best_count'], 	\
			item['comment_good_count'], 	\
			item['comment_bad_count'], 		\
			item['editor_comment'], 		\
			item['desc_info'], 		\
			item['score'], 		\
			item['feature'], 		\
			) 
		self.file.write(line)
		
		return item
