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
		# line = json.dumps(dict(item)) + '\n'
		# self.file.write(line.decode("unicode_escape"))

		# tsv格式存储
		line =  "%s\t%d\t%s\t%s\t%d\t%d\t%s\t%s\t%s\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%s\t%s" % ( 		\
			item['channel'], 		\
			item['crawl_time'], 	\
			item['crawl_url'], 	\
			item['name'], 	\
			item['size'], 	\
			item['update_time'], 	\
			item['category'], 	\
			item['tag'], 	\
			item['version'], 	\
			item['system'], 	\
			item['source'], 	\
			item['install_count'], 	\
			item['like_count'], 	\
			item['comment_count'], 	\
			item['comment_best_count'], 	\
			item['comment_good_count'], 	\
			item['comment_bad_count'], 	\
			item['editor_comment'], 	\
			item['desc_info'] 	\
			) 
		self.file.write(line)
		

		return item
