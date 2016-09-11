****

#	<center>app-basket</center>
##### <center>Author: HouJP_NSD</center>
##### <center>E-mail: houjp1992@gmail.com</center>

****

##	目录
*	[项目介绍](#intro)
*	[使用说明](#usage)
*	[版本更新](#version)

****

##	<a name="intro">项目介绍</a>

基于scrapy框架完成的APP爬虫，用于收集安卓系统下各类应用的基本信息。


###	字段说明

### 数据说明

已爬取的数据信息如下：

| 数据来源 | 数据条数 | 目录位置 |
| ---- | ---- | ---- |
| 豌豆荚 | 504,518 | data/wandoujia.tsv |

目前爬取的信息包含以下字段：

|字段名|	类型|	描述|	样例|
|---- |---- |---- |---- |
|channel|	String|	爬取渠道|	豌豆荚/百度/360|
|crawl_time|	Long|	爬取时间	|11231230|
|crawl_url|	String	|爬取链接|	http://www.wandoujia.com/apps/com.sdu.didi.psnger|
|name|	String	|应用名字|	滴滴出行|
|size|	Long	|应用大小（B）|	56|
|update_time|	Long	|更细时间	|10231231|
|category|	String	|所属类别|	交通导航-打车|
|tag|	String	|标签|	休闲-模拟-像素-驾驶-生活应用-上瘾-日常出行-男性|
|version|	String	|版本信息|	4.4.4|
|system|	String|	手机系统要求|	Android 4.0.3 以上|
|source|	String|	软件来源	|北京小桔科技有限公司|
|install_count|	Int	|安装人数/下载人数|	27480000|
|like_count|	Int|	喜欢人数|	4421|
|comment_count|	Int	|评论人数|	3424|
|comment_best_count|	Int|	好评数|	342|
|comment_good_count|	Int	|中评数|	314|
|comment_bad_count|	Int	|差评数|	312|
|editor_comment|	String|	小编点评	|用滴滴叫出租车，都市畅行无阻。滴滴一下，美好出行！|
|desc_info|	String	|描述	|（省略）|
|score|	Int	|评分（100分制）	|80|
|feature|	String	|特性	|官方版-安全-优质-MTC认证|


****

##	<a name="usage">使用说明</a>







****

##	<a name="version">版本更新</a>

*	2016-09-11
	*	完成【百度手机助手】站点HTML解析
*	2016-09-05
	*	完成【豌豆荚】站点HTML解析

****

