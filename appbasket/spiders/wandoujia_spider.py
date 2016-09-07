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

class WandoujiaSpider(scrapy.Spider):

    # 爬取间隔1s
    # download_delay = 1
    # 爬虫名字
    name = "wandoujia"
    # 限制范围
    allowed_domains = ["www.wandoujia.com/apps/"]
    # 种子URL
    start_urls = [
        #"http://www.wandoujia.com/apps/zhangyu.spirited.away.puzzle",
        # "http://www.wandoujia.com/apps/com.tencent.mm03",
        ]

    def __init__(self):
        # 载入start_urls
        self.loadStartURLs()

        # 统计处理url总数
        self.urls_sum = 0L

        return

    # 载入start_urls
    def loadStartURLs(self):
        prefix = "http://www.wandoujia.com/apps/"
        # 文件URL
        file = open('data/apps.txt', 'r')
        for line in file:
            self.start_urls.append(prefix + StrUtil.delWhiteSpace(line))
        file.close()

        # 固定URL
        # self.start_urls.append("http://www.wandoujia.com/apps/air.jp.funkyland.AliceHouse2")
        # self.start_urls.append("http://www.wandoujia.com/apps/com.tencent.mm")

        return

    # 解析函数
    def parse(self, response):

        selector = scrapy.Selector(response)

        # APP信息容器
        yield self.getItem(selector, response)

        # 递归搜索URL
        # relateApp_urls = selector.xpath('//a[@data-track="detail-click-relateApp"]/@href').extract()
        # for url in relateApp_urls:
        #     print url
        #     yield Request(url, callback=self.parse)

        # 已处理URL数目统计
        self.urls_sum += 1
        LogUtil.log("urls_sum(%d)" % self.urls_sum)

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

        return item

    # 获取渠道
    def getChannel(self, selector, item):
        item['channel'] = "豌豆荚"

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
        xpath = '//p[@class="app-name"]/span[@class="title" and @itemprop="name"]/text()'

        eles = selector.xpath(xpath).extract()

        name = "NULL"
        if (0 != len(eles)):
            name = eles[0]

        item['name'] = StrUtil.delWhiteSpace(name)
        LogUtil.log("name(%s)" % item['name'])

        return

    # 获取软件大小(B)
    def getSize(self, selector, item):
        xpath = '//meta[@itemprop="fileSize"]/@content'

        eles = selector.xpath(xpath).extract()

        size = -1L
        if (0 != len(eles)):
            size = long(eles[0])

        item['size'] = size
        LogUtil.log("size(%d)" % item['size'])

        return

    # 获取软件版本更新时间
    def getUpdateTime(self, selector, item):
        xpath = '//time[@itemprop="datePublished"]/text()'

        eles = selector.xpath(xpath).extract()

        update_time = -1L
        if (0 != len(eles)):
            d = datetime.datetime.strptime(eles[0],"%Y年%m月%d日")
            update_time = long(time.mktime(d.timetuple()))
        item['update_time'] = update_time

        LogUtil.log("update_time(%d)" % item['update_time'])

        return

    # 获取软件标签
    def getTag(self, selector, item):
        xpath = '//div[@class="side-tags clearfix"]/div/a/text()'

        tag = ""
        tags = selector.xpath(xpath).extract()
        for i in range(len(tags)):
            if (i):
                tag = tag + "-" + StrUtil.delWhiteSpace(tags[i])
            else:
                tag = StrUtil.delWhiteSpace(tags[i])
        
        if (0 != len(tag)):
            item['tag'] = tag
        else:
            item['tag'] = "NULL"

        LogUtil.log("tag(%s)" % item['tag'])

        return

    # 获取类别信息
    def getCategory(self, selector, item):
        xpath = '//dd[@class="tag-box"]/a/text()'

        category = ""
        categories = selector.xpath(xpath).extract()
        for i in range(len(categories)):
            if (i):
                category = category + "-" + StrUtil.delWhiteSpace(categories[i])
            else:
                category = StrUtil.delWhiteSpace(categories[i])
        
        if (0 != len(category)):
            item['category'] = category
        else:
            item['category'] = "NULL"

        LogUtil.log("category(%s)" % item['category'])    

        return

    # 获取版本信息
    def getVersion(self, selector, item):
        # xpath = '//dl[@class="infos-list"]/dd[5]/text()'
        xpath = u'//dl[@class="infos-list"]/dt[text() = "版本"]/following::*[1]/text()'
        eles = selector.xpath(xpath).extract()

        if (0 != len(eles)):
            item['version'] = StrUtil.delWhiteSpace(eles[0])
        else:
            item['version'] = "NULL"

        LogUtil.log("version(%s)" % item['version'])    

        return

    # 获取系统信息
    def getSystem(self, selector, item):
        xpath = '//dd[@itemprop="operatingSystems"]/text()'

        eles = selector.xpath(xpath).extract()

        system = "NULL"
        if (0 != len(eles)):
            pattern = re.compile('\s+')
            system = (re.sub(pattern,' ',eles[0])).strip()
        item['system'] = system

        LogUtil.log("system(%s)" % item['system'])    

        return

    # 获取来源信息
    def getSource(self, selector, item):
        # xpath = '//a[@itemprop="url" and @class="dev-sites"]/span/text()'
        xpath = u'//dl[@class="infos-list"]/dt[text() = "来自"]/following::*[1]'

        eles = selector.xpath(xpath).xpath('string(.)').extract()

        source = "NULL"
        if (0 != len(eles)):
            pattern = re.compile('\s+')
            source = (re.sub(pattern,' ',eles[0])).strip()
        item['source'] = source

        LogUtil.log("source(%s)" % item['source'])    

        return

    # 获取安装人数
    def getInstallCount(self, selector, item):
        xpath = '//i[@itemprop="interactionCount"]/text()'

        eles = selector.xpath(xpath).extract()

        install_count = -1L
        if (0 != len(eles)):
            pattern = re.compile('\s+')
            install_count_str = (re.sub(pattern,' ',eles[0])).strip()
            arr = install_count_str.split(" ")
            if (1 == len(arr)):
                install_count = float(arr[0])
            else:
                install_count = float(arr[0]) * self.unitToNum(arr[1])
        item['install_count'] = long(install_count)

        LogUtil.log("install_count(%d)" % item['install_count'])    

        return

    # 获取喜欢人数
    def getLikeCount(self, selector, item):
        xpath = '//span[@class="item love"]/i/text()'

        eles = selector.xpath(xpath).extract()

        like_count = -1L
        if (0 != len(eles)):
            pattern = re.compile('\s+')
            num_str = (re.sub(pattern,' ',eles[0])).strip()
            arr = num_str.split(" ")
            if (1 == len(arr)):
                like_count = float(arr[0])
            else:
                like_count = float(arr[0]) * self.unitToNum(arr[1])
        item['like_count'] = long(like_count)

        LogUtil.log("like_count(%d)" % item['like_count'])    

        return

    # 获取评论人数
    def getCommentCount(self, selector, item):
        xpath = '//a[@class="item last comment-open"]/i/text()'

        eles = selector.xpath(xpath).extract()

        comment_count = -1L
        if (0 != len(eles)):
            comment_count = self.strToNum(eles[0])
        item['comment_count'] = comment_count

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
        xpath = '//div[@class="editorComment"]/div/text()'

        eles = selector.xpath(xpath).extract()

        editor_comment = "NULL"
        if (0 != len(eles)):
            editor_comment = eles[0]
        item['editor_comment'] = StrUtil.delWhiteSpace(editor_comment)

        LogUtil.log("editor_comment(%s)" % item['editor_comment'])    

        return

    # 获取软件描述
    def getDescInfo(self, selector, item):
        xpath = '//div[@itemprop="description"]//text()'

        eles = selector.xpath(xpath).extract()
        # eles = selector.xpath(xpath).xpath('string(., " ")').extract()

        desc_info = "NULL"
        if (0 != len(eles)):
            desc_info = " ".join(eles)
        item['desc_info'] = StrUtil.delWhiteSpace(desc_info)

        LogUtil.log("desc_info(%s)" % item['desc_info'])    

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
