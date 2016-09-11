# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import scrapy
from scrapy.http import Request
import logging
import time, datetime
from appbasket.items import AppbasketItem
from appbasket.utils import StrUtil
from appbasket.utils import LogUtil

class BaiduSpider(scrapy.Spider):

	# 爬虫名字
    name = "baidu"
    # 域名
    domain = "http://shouji.baidu.com"
    # 限制范围
    allowed_domains = ["shouji.baidu.com"]
    # 种子URL
    start_urls = []

    def __init__(self):
        # 载入start_urls
        self.loadStartURLs()

        # 统计处理url总数
        self.urls_sum = 0L

        return

    # 载入start_urls
    def loadStartURLs(self):

        # 固定URL
        self.start_urls.append("http://shouji.baidu.com/software/") # 安卓软件
        self.start_urls.append("http://shouji.baidu.com/game/") # 安卓游戏
        # self.start_urls.append("http://shouji.baidu.com/software/503_board_100_01/") # 聊天软件
        # self.start_urls.append("http://shouji.baidu.com/software/9935187.html")
        return

    # 解析函数
    def parse(self, response):

        selector = scrapy.Selector(response)

        # APP信息容器
        yield self.getItem(selector, response)

        # 提取各类别首页链接
        for url in self.getCateLink(selector):
        	print url
        	yield Request(url, callback=self.parse)

        # 提取App详情页面链接
        for url in self.getAppLink(selector):
        	print url
        	yield Request(url, callback=self.parse)

        # 提取翻页链接
        for url in self.getPageLink(selector, str(response.url).encode('utf-8')):
        	print url
        	yield Request(url, callback=self.parse)

        # 提取相关网页链接
        for url in self.getRelateLink(selector):
        	print url
        	yield Request(url, callback=self.parse)

        # 已处理URL数目统计
        self.urls_sum += 1
        LogUtil.log("urls_sum(%d)" % self.urls_sum)

    # URL处理函数：
    #   1. 去除空白符
    #   2. 补全域名
    def treatURL(self, url):

        url = url.strip()
        if (-1 == url.find(self.domain)):
            url = self.domain + url

        return url

    # 提取各类别首页链接
    def getCateLink(self, selector):
        xpath = '//li[contains(@class, "cate-item")]//a/@href'

        eles = selector.xpath(xpath).extract()

        return filter(StrUtil.isEmpty, map(self.treatURL, eles))

    # 提取App详情页面链接
    def getAppLink(self, selector):
        xpath = '//div[@class="app-box"]/a/@href'

        eles = selector.xpath(xpath).extract()

        return filter(StrUtil.isEmpty, map(self.treatURL, eles))

    # 提取各类别页面中翻页链接
    def getPageLink(self, selector, prefix):
        xpath = '//div[@class="pager"]//a/@href'

        eles = selector.xpath(xpath).extract()
        for i in range(len(eles)):
        	eles[i] = StrUtil.completeURL(prefix, eles[i])

        return filter(StrUtil.isEmpty, eles)

    # 提取相关软件链接
    def getRelateLink(self, selector):
        xpath = '//div[@class="app-bd show"]//a[@class="app-box"]/@href'

        eles = selector.xpath(xpath).extract()

        return filter(StrUtil.isEmpty, map(self.treatURL, eles))

    # 提取Item
    def getItem(self, selector, response):
        # 新建信息容器
        item = AppbasketItem()

        # 更新信息
        self.getChannel(selector, item)
        self.getCrawlTime(selector, item)
        self.getCrawlURL(selector, item, response)
        self.getName(selector, item)
        self.getSize(selector, item)
        self.getUpdateTime(selector, item)
        self.getTag(selector, item)
        self.getCategory(selector, item)
        self.getVersion(selector, item)
        self.getSystem(selector, item)
        self.getSource(selector, item)
        self.getInstallCount(selector, item)
        self.getLikeCount(selector, item)
        self.getCommentCount(selector, item)
        self.getCommentBestCount(selector, item)
        self.getCommentGoodCount(selector, item)
        self.getCommentBadCount(selector, item)
        self.getEditorComment(selector, item)
        self.getDescInfo(selector, item)
        self.getScore(selector, item)
        self.getFeature(selector, item)

        return item

    # 获取渠道
    def getChannel(self, selector, item):
        item['channel'] = "百度手机助手"

        LogUtil.log("channel(%s)" % item['channel'])

        return

    # 获取爬取时间
    def getCrawlTime(self, selector, item):
        item['crawl_time'] = long(time.time())

        LogUtil.log("crawl_time(%d)" % item['crawl_time'])

        return

    # 获取爬取url
    def getCrawlURL(self, selector, item, response):
        item['crawl_url'] = str(response.url).encode('utf-8')

        LogUtil.log("crawl_url(%s)" % item['crawl_url'])

        return

    # 获取软件名
    def getName(self, selector, item):
        xpath = '//div[@class="app-intro"]//h1[@class="app-name"]/span/text()'

        eles = selector.xpath(xpath).extract()

        name = "NULL"
        if (0 != len(eles)):
            name = eles[0]

        item['name'] = StrUtil.delWhiteSpace(name)
        LogUtil.log("name(%s)" % item['name'])

        return

    # 获取软件大小(B)
    def getSize(self, selector, item):
        xpath = '//div[@class="app-intro"]//span[@class="size"]/text()'

        eles = selector.xpath(xpath).extract()

        size = -1

        while True :
        	if (0 == len(eles)):
        		break
        	string = eles[0]
        	nums = re.findall(r"\d+\.?\d*", string)
        	if (0 == len(nums)):
        		break
        	size = float(nums[0])
        	if (-1 != string.find('K')):
        		size *= 1024 
        	if (-1 != string.find('M')):
        		size *= 1024 * 1024
        	if (-1 != string.find('G')):
        		size *= 1024 * 1024 * 1024
        	break

        item['size'] = long(size)
        LogUtil.log("size(%d)" % item['size'])

        return

    # 获取软件版本更新时间
    def getUpdateTime(self, selector, item):
        
        item['update_time'] = -1

        LogUtil.log("update_time(%d)" % item['update_time'])

        return

    # 获取软件标签
    def getTag(self, selector, item):
        
    	item['tag'] = "NULL"

        LogUtil.log("tag(%s)" % item['tag'])

        return

    # 获取类别信息
    def getCategory(self, selector, item):
        xpath = '//div[@class="app-nav"]//a/text()'

        category = "NULL"

        while True:

        	strings = selector.xpath(xpath).extract()
        	if (1 >= len(strings)):
        		break
        	category = "-".join(map(StrUtil.delWhiteSpace, strings[1:]))

        	break

        item['category'] = category

        LogUtil.log("category(%s)" % item['category'])    

        return

    # 获取版本信息
    def getVersion(self, selector, item):
        xpath = '//div[@class="app-intro"]//span[@class="version"]/text()'

        eles = selector.xpath(xpath).extract()

        item['version'] = "NULL"

        while True:
        	if (0 == len(eles)):
        		break
        	string = eles[0]
        	nums = re.findall(r"\d+[\.\d+]*", string)
        	if (0 == len(nums)):
        		break
        	item['version'] = nums[0]

        	break

        LogUtil.log("version(%s)" % item['version'])    

        return

    # 获取系统信息
    def getSystem(self, selector, item):
       
        item['system'] = "NULL"

        LogUtil.log("system(%s)" % item['system'])    

        return

    # 获取来源信息
    def getSource(self, selector, item):
        xpath = '//div[@class="app-intro"]//div[@class="origin-wrap"]//a[@class="origin"]/text()'

        item['source'] = "NULL"

        while True:
        	eles = selector.xpath(xpath).extract()

        	if (0 == len(eles)):
        		break
        	string = eles[0]
        	item['source'] = StrUtil.delWhiteSpace(string)

        	break

        LogUtil.log("source(%s)" % item['source'])    

        return

    # 获取安装人数
    def getInstallCount(self, selector, item):
        xpath = '//div[@class="app-intro"]//span[@class="download-num"]/text()'

        item['install_count'] = -1L

        while True:
        	eles = selector.xpath(xpath).extract()
        	if (0 == len(eles)):
        		break
        	string = eles[0]
        	nums = re.findall(r"\d+\.?\d*", string)
        	if (0 == len(nums)):
        		break
        	num = float(nums[0])
        	if (-1 != string.find('亿')):
        		num *= 1e8
        	if (-1 != string.find('万')):
        		num *= 1e4
        	if (-1 != string.find('千')):
        		num *= 1e3
        	item['install_count'] = long(num)
        	break

        LogUtil.log("install_count(%d)" % item['install_count'])    

        return

    # 获取喜欢人数
    def getLikeCount(self, selector, item):

        item['like_count'] = -1L

        LogUtil.log("like_count(%d)" % item['like_count'])    

        return

    # 获取评论人数
    def getCommentCount(self, selector, item):
        
        item['comment_count'] = -1L

        LogUtil.log("comment_count(%d)" % item['comment_count'])    

        return

    # 获取好评数
    def getCommentBestCount(self, selector, item):
        item['comment_best_count'] = -1L

        LogUtil.log("comment_best_count(%d)" % item['comment_best_count'])    

        return

    # 获取中评数
    def getCommentGoodCount(self, selector, item):
        item['comment_good_count'] = -1L

        LogUtil.log("comment_good_count(%d)" % item['comment_good_count'])    

        return

    # 获取差评数
    def getCommentBadCount(self, selector, item):
        item['comment_bad_count'] = -1L

        LogUtil.log("comment_bad_count(%d)" % item['comment_bad_count'])    

        return

    # 获取编辑评论
    def getEditorComment(self, selector, item):
        xpath = '//div[@class="app-detail"]//span[@class="head-content"]/text()'

        eles = selector.xpath(xpath).extract()

        editor_comment = "NULL"
        if (0 != len(eles)):
            editor_comment = eles[0]
        item['editor_comment'] = StrUtil.delWhiteSpace(editor_comment)

        LogUtil.log("editor_comment(%s)" % item['editor_comment'])    

        return

    # 获取软件描述
    def getDescInfo(self, selector, item):
        xpath = '//div[@class="app-detail"]//div[@class="brief-long"]/p//text()'

        eles = selector.xpath(xpath).extract()
        # eles = selector.xpath(xpath).xpath('string(., " ")').extract()

        desc_info = "NULL"
        if (0 != len(eles)):
            desc_info = " ".join(eles)
        item['desc_info'] = StrUtil.delWhiteSpace(desc_info)

        LogUtil.log("desc_info(%s)" % item['desc_info'])    

        return

      # 获取评分
    def getScore(self, selector, item):
    	xpath = '//div[@class="app-feature"]//span[@class="star-percent"]/@style'
        
        item['score'] = -1

        while True:
        	eles = selector.xpath(xpath).extract()
        	if (0 == len(eles)):
        		break
        	string = eles[0]
        	nums = re.findall(r"\d+\.?\d*", string)
        	if (0 == nums):
        		break
        	item['score'] = int(nums[0])

        	break

        LogUtil.log("score(%d)" % item['score'])

        return  

    # 获取特性
    def getFeature(self, selector, item):
        xpath = '//div[@class="yui3-g"]//div[@class="app-feature"]//span[@class="app-feature-detail"]//text()'

        item['feature'] = "NULL"

        while True:
        	eles = selector.xpath(xpath).extract()
        	item['feature'] = "-".join(filter(StrUtil.isEmpty, map(StrUtil.delWhiteSpace, eles)))

        	break

        LogUtil.log("feature(%s)" % item['feature'])

        return    

    # 含有文字单位的数字字符串转数字，例如："345 万" --> 3450000L
    def strToNum(self, n_str):
        pattern = re.compile('\s+')
        n_str = (re.sub(pattern,' ', n_str)).strip()
        arr = n_str.split(" ")
        if (1 == len(arr)):
            return long(float(arr[0]))
        else:
            return long(float(arr[0]) * self.unitToNum(arr[1]))

    # 文字单位转数字，例如："万" --> 10000L
    def unitToNum(self, unit):
        if ("万" == unit):
            return long(1e4)
        elif ("亿" == unit):
            return long(1e8)
        else:
            return 1L
