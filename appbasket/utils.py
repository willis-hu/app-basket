# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

# 字符串工具
class StrUtil(object):
	def __init__(self):
		pass

	# 删除字符串中的空白符，连续空白符用空格代替
	@staticmethod
	def delWhiteSpace(msg):
		pattern = re.compile('\s+')
		return (re.sub(pattern, ' ', msg)).strip()

	# 判断字符串是否为空
	@staticmethod
	def isEmpty(msg):
		return msg and msg.strip()

	# 判断URL是否包含prefix并补全
	@staticmethod
	def completeURL(prefix, url):
		url = url.strip()
		if (-1 == url.find(prefix)):
			url = prefix + url

		return url

# 日志工具
class LogUtil(object):
	def __init__(self):
		pass

	@staticmethod
	def log(msg):
		print "HouJP >> " + str(msg)
		return