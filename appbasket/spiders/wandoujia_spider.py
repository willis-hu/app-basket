# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import scrapy
import logging
import time, datetime
from appbasket.items import AppbasketItem

class WandoujiaSpider(scrapy.Spider):

    # 爬取间隔1s
    download_delay = 1
    # 爬虫名字
    name = "wandoujia"
    # 限制范围
    allowed_domains = ["www.wandoujia.com/apps/", "wandoujia.com/apps/"]
    # 种子URL
    start_urls = [
        "http://www.wandoujia.com/apps/com.tencent.mm#comments",
        ]

    # 解析函数
    def parse(self, response):

        selector = scrapy.Selector(response)

        # APP信息容器
        item = self.getItem(selector, response)

        # 递归搜索URL
        relateApp_urls = selector.xpath('//a[@data-track="detail-click-relateApp"]/@href').extract()
        for url in relateApp_urls:
            print url
        
        return

    # 提取Item
    def getItem(self, selector, response):
        # 新建信息容器
        item = AppbasketItem()

        # 更新信息
        item['channel'] = "豌豆荚"
        item['crawl_time'] = long(time.time())
        item['crawl_url'] = str(response.url).encode('utf-8')
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
        item['comment_best_count'] = -1L
        item['comment_good_count'] = -1L
        item['comment_bad_count'] = -1L
        self.getEditorComment(selector, item)
        self.getDescInfo(selector, item)

        return item

    # 获取软件名
    def getName(self, selector, item):
        xpath = '//span[@class="title"]/text()'

        eles = selector.xpath(xpath).extract()

        name = "NULL"
        if (0 != len(eles)):
            name = eles[0]

        item['name'] = name

        return

    # 获取软件大小(B)
    def getSize(self, selector, item):
        xpath = '//meta[@itemprop="fileSize"]/@content'

        eles = selector.xpath(xpath).extract()

        size = -1L
        if (0 != len(eles)):
            size = long(eles[0])

        item['size'] = size

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

        return

    # 获取软件标签
    def getTag(self, selector, item):
        xpath = '//div[@class="side-tags clearfix"]/div/a/text()'

        tag = ""
        tags = selector.xpath(xpath).extract()
        for i in range(len(tags)):
            if (i):
                tag = tag + "-" + tags[i].strip()
            else:
                tag = tags[i].strip()
        
        if (0 != len(tag)):
            item['tag'] = tag
        else:
            item['tag'] = "NULL"

        return

    # 获取类别信息
    def getCategory(self, selector, item):
        xpath = '//dd[@class="tag-box"]/a/text()'

        category = ""
        categories = selector.xpath(xpath).extract()
        for i in range(len(categories)):
            if (i):
                category = category + "-" + categories[i].strip()
            else:
                category = categories[i].strip()
        
        if (0 != len(category)):
            item['category'] = category
        else:
            item['category'] = "NULL"

        return

    # 获取版本信息
    def getVersion(self, selector, item):
        xpath = '//dl[@class="infos-list"]/dd[5]/text()'
        eles = selector.xpath(xpath).extract()

        if (0 != len(eles)):
            item['version'] = eles[0]
        else:
            item['version'] = "NULL"

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

        return

    # 获取来源信息
    def getSource(self, selector, item):
        xpath = '//a[@itemprop="url" and @class="dev-sites"]/span/text()'

        eles = selector.xpath(xpath).extract()

        source = "NULL"
        if (0 != len(eles)):
            pattern = re.compile('\s+')
            source = (re.sub(pattern,' ',eles[0])).strip()
        item['source'] = source

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
                install_count = long(arr[0])
            else:
                install_count = long(arr[0]) * self.unitToNum(arr[1])
        item['install_count'] = install_count

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
                like_count = long(arr[0])
            else:
                like_count = long(arr[0]) * self.unitToNum(arr[1])
        item['like_count'] = like_count

        return

    # 获取评论人数
    def getCommentCount(self, selector, item):
        xpath = '//a[@class="item last comment-open"]/i/text()'

        eles = selector.xpath(xpath).extract()

        comment_count = -1L
        if (0 != len(eles)):
            comment_count = self.strToNum(eles[0])
        item['comment_count'] = comment_count

        return

    # 获取编辑评论
    def getEditorComment(self, selector, item):
        xpath = '//div[@class="editorComment"]/div/text()'

        eles = selector.xpath(xpath).extract()

        editor_comment = "NULL"
        if (0 != len(eles)):
            editor_comment = eles[0]
        item['editor_comment'] = editor_comment

        return

    # 获取软件描述
    def getDescInfo(self, selector, item):
        xpath = '//div[@itemprop="description"]'

        eles = selector.xpath(xpath).xpath('string(.)').extract()

        desc_info = "NULL"
        if (0 != len(eles)):
            desc_info = eles[0]
        item['desc_info'] = desc_info

        return

    # 含有文字单位的数字字符串转数字，例如："345 万" --> 3450000L
    def strToNum(self, n_str):
        pattern = re.compile('\s+')
        n_str = (re.sub(pattern,' ', n_str)).strip()
        arr = n_str.split(" ")
        if (1 == len(arr)):
            return long(arr[0])
        else:
            return long(arr[0]) * self.unitToNum(arr[1])

    # 文字单位转数字，例如："万" --> 10000L
    def unitToNum(self, unit):
        if ("万" == unit):
            return long(1e4)
        elif ("亿" == unit):
            return long(1e8)
        else:
            return 1L

    # 日志函数
    def log(self, msg):
        print "HouJP >> [" + str(type(msg)) + "] " + "[size: " + str(len(msg)) + "] " + str(msg)

        return
