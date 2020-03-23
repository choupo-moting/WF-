# -*- coding: utf-8 -*-
import scrapy, re
from lxml.html import etree
from WangFang.items import MeetingItem
from scrapy_redis.spiders import RedisCrawlSpider


class MeetingSpider(scrapy.Spider):
    # class MeetingSpider(RedisCrawlSpider):
    name = 'meeting'
    allowed_domains = ['wanfangdata.com.cn']
    start_urls = ['http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%94%BF%E6%B2%BB%20DBID%3AWF_HY&f=top&p=1',
                  'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_HY&f=top&p=1']

    # http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_HY&f=top
    # redis_key = 'meeting:start_urls'
    def parse(self, response):
        if response:

            if '%E6%B3%95%E5%BE%8B' in response.url:  # 法律
                ID_list = response.xpath('.//div[@class="record-item-list"]/div[@class="record-item"]')
                for ID in ID_list:
                    # 从原版的详情的url上获取详情ID，然后拼接
                    id = \
                    (ID.xpath('.//div[@class="record-title"]/a[@class="title"]/@href').extract_first('').split('/'))[-1]
                    print(id)
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=conference&id={}'.format(id)
                    # http://www.wanfangdata.com.cn/details/detail.do?_type=conference&id=9516620
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.parse_laws_data
                    )
                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()) > 4:
                #     print(len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()),
                #           '=================')
                next_url = 'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_HY&f=top&p={}'.format(
                    int(page) + 1)
                print('开始爬取学位下法律第{}页================================================================='.format(page))

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
                # else:
                #     print('学科法律数据爬取完毕！')

            if '%E6%94%BF%E6%B2%BB' in response.url:  # 政治
                ID_list = response.xpath('.//div[@class="record-item-list"]/div[@class="record-item"]')
                for ID in ID_list:
                    # 从原版的详情的url上获取详情ID，然后拼接
                    id = \
                    (ID.xpath('.//div[@class="record-title"]/a[@class="title"]/@href').extract_first('').split('/'))[-1]
                    print(id)
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=conference&id={}'.format(id)
                    # http://www.wanfangdata.com.cn/details/detail.do?_type=conference&id=9516620
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.parse_zhengzhi_data
                    )
                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()) > 4:
                #     print(len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()),
                #           '=================')
                next_url = 'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%94%BF%E6%B2%BB%20DBID%3AWF_HY&f=top&p={}'.format(
                    int(page) + 1)
                print('开始爬取学位下法律第{}页================================================================='.format(page))

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
                # else:
                #     print('学科法律数据爬取完毕！')

    def parse_laws_data(self, response):

        """
        #类别号
        classes_num = scrapy.Field()
        # 中文标题
        chinese_title = scrapy.Field()
        # 摘要
        abstract = scrapy.Field()
        # 关键语
        chinese_key = scrapy.Field()
        # 作者
        author_chinaese = scrapy.Field()
        # 作者单位
        author_dw = scrapy.Field()
        # 母体文献
        literature = scrapy.Field()
        # 会议名称
        meeting_name = scrapy.Field()
        # 会议时间 
        meeting_time = scrapy.Field()
        # 会议地点
        meeting_address = scrapy.Field()
        # 主办单位
        sponsor = scrapy.Field()
        # 语种
        language = scrapy.Field()
        # 分类号
        classes_mark = scrapy.Field()
        # 在线出版日期
        online_date = scrapy.Field()
        # 页码
        page_mark = scrapy.Field()
        :param response:
        :return:
        """
        # print(response.text)
        item = MeetingItem()
        item['classes_num'] = 0
        item['chinese_title'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r', '').replace(
            '\t', '').replace('\n', '')
        item['abstract'] = response.xpath('//div[@id="see_alldiv"]/text()').extract_first('暂无').replace('\r',
                                                                                                        '').replace(
            '\t', '').replace('\n', '')
        list_info = response.xpath('//div[@class="left_con_top"]/ul//li/div[1]/text()').extract()
        print(list_info)
        if '关键词：' in list_info:
            panten = re.compile('<div\sclass="info_left">关键词：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['chinese_key'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')
        if '作者：' in list_info:
            panten = re.compile('<div\sclass="info_left">作者：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['author_chinaese'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                   '').replace(
                '\n', '')
        if '作者单位：' in list_info:
            panten = re.compile('<div\sclass="info_left">作者单位：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['author_dw'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '母体文献：' in list_info:
            panten = re.compile('<div\sclass="info_left">母体文献：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['literature'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                              '').replace(
                '\n', '')
        if '会议名称：' in list_info:
            panten = re.compile('<div\sclass="info_left">会议名称：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['meeting_name'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '会议时间：' in list_info:
            panten = re.compile('<div\sclass="info_left">会议时间：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['meeting_time'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '会议地点：' in list_info:
            panten = re.compile('<div\sclass="info_left">会议地点：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['meeting_address'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                   '').replace(
                '\n', '')
        if '主办单位：' in list_info:
            panten = re.compile('<div\sclass="info_left">主办单位：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['sponsor'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                           '').replace(
                '\n', '')
        if '语 种：' in list_info:
            panten = re.compile('<div\sclass="info_left">语 种：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['language'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                            '').replace(
                '\n', '')
        if '分类号：' in list_info:
            panten = re.compile('<div\sclass="info_left">分类号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['classes_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '在线出版日期：' in list_info:
            panten = re.compile('<div\sclass="info_left">在线出版日期：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['online_date'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')
        if '页码：：' in list_info:
            panten = re.compile('<div\sclass="info_left">页码：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['page_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')

        yield item

    def parse_zhengzhi_data(self, response):
        item = MeetingItem()
        item['classes_num'] = 1
        item['chinese_title'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r', '').replace(
            '\t', '').replace('\n', '')
        item['abstract'] = response.xpath('//div[@id="see_alldiv"]/text()').extract_first('暂无').replace('\r',
                                                                                                        '').replace(
            '\t', '').replace('\n', '')
        list_info = response.xpath('//div[@class="left_con_top"]/ul//li/div[1]/text()').extract()
        print(list_info)
        if '关键词：' in list_info:
            panten = re.compile('<div\sclass="info_left">关键词：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['chinese_key'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')
        if '作者：' in list_info:
            panten = re.compile('<div\sclass="info_left">作者：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['author_chinaese'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                   '').replace(
                '\n', '')
        if '作者单位：' in list_info:
            panten = re.compile('<div\sclass="info_left">作者单位：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['author_dw'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '母体文献：' in list_info:
            panten = re.compile('<div\sclass="info_left">母体文献：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['literature'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                              '').replace(
                '\n', '')
        if '会议名称：' in list_info:
            panten = re.compile('<div\sclass="info_left">会议名称：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['meeting_name'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '会议时间：' in list_info:
            panten = re.compile('<div\sclass="info_left">会议时间：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['meeting_time'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '会议地点：' in list_info:
            panten = re.compile('<div\sclass="info_left">会议地点：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['meeting_address'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                   '').replace(
                '\n', '')
        if '主办单位：' in list_info:
            panten = re.compile('<div\sclass="info_left">主办单位：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['sponsor'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                           '').replace(
                '\n', '')
        if '语 种：' in list_info:
            panten = re.compile('<div\sclass="info_left">语 种：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['language'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                            '').replace(
                '\n', '')
        if '分类号：' in list_info:
            panten = re.compile('<div\sclass="info_left">分类号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['classes_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '在线出版日期：' in list_info:
            panten = re.compile('<div\sclass="info_left">在线出版日期：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['online_date'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')
        if '页码：：' in list_info:
            panten = re.compile('<div\sclass="info_left">页码：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['page_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')

        yield item
