# -*- coding: utf-8 -*-
import scrapy, re
from lxml.html import etree
from WangFang.items import DegreeItem
from scrapy_redis.spiders import RedisCrawlSpider


class DegreeSpider(scrapy.Spider):
# class DegreeSpider(RedisCrawlSpider):
    name = 'degree'
    allowed_domains = ['wanfangdata.com.cn']
    start_urls = ['http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%94%BF%E6%B2%BB%20DBID%3AWF_XW&f=top&p=1',
                  'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_XW&f=top&p=1']
    # redis_key = 'degree:start_urls'

    def parse(self, response):
        if response:
            if '%E6%B3%95%E5%BE%8B' in response.url:  # 法律
                ID_list = response.xpath('.//div[@class="record-item-list"]/div[@class="record-item"]')
                for ID in ID_list:
                    # 从原版的详情的url上获取详情ID，然后拼接
                    id = \
                    (ID.xpath('.//div[@class="record-title"]/a[@class="title"]/@href').extract_first('').split('/'))[-1]
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=degree&id={}'.format(id)
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.parse_laws_data
                    )
                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//p[@class="pager"]/a').extract()) > 4:
                #     print(len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()),'=================')
                next_url = 'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_XW&f=top&p={}'.format(
                    int(page) + 1)
                print('开始爬取学位下法律第{}页================================================================='.format(page))

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
            if '%E6%94%BF%E6%B2%BB' in response.url:
                ID_list = response.xpath('.//div[@class="record-item-list"]/div[@class="record-item"]')
                for ID in ID_list:
                    # 从原版的详情的url上获取详情ID，然后拼接
                    id = \
                    (ID.xpath('.//div[@class="record-title"]/a[@class="title"]/@href').extract_first('').split('/'))[-1]
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=degree&id={}'.format(id)
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.prase_politics_data
                    )
                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//p[@class="pager"]/a').extract()) > 4:
                #     print(len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()),
                #           '=================')
                next_url = 'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%94%BF%E6%B2%BB%20DBID%3AWF_XW&f=top&p={}'.format(
                    int(page) + 1)
                print('开始爬取学位下政治第{}页================================================================='.format(page))

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
        else:
            print('爬虫结束')

    def parse_laws_data(self, response):
        """
        classes_num = scrapy.Field()
        # 中文标题
        chinaese_title = scrapy.Field()
        # 中文关键词
        chinaese_key = scrapy.Field()
        # 中文作者名 
        chinaese_name = scrapy.Field()
        # 学位授权单位
        degree_dw = scrapy.Field()
        # 授予学位
        degree_sy = scrapy.Field()
        # 学科专业
        degree_profession = scrapy.Field()
        # 导师姓名
        teacher_name = scrapy.Field()
        # 学位年度
        degree_year = scrapy.Field()
        # 语种  
        language = scrapy.Field()
        # 分类号  
        classes_mark = scrapy.Field()
        # 在线出版日期  
        create_time = scrapy.Field()
        :param response:
        :return:
        """
        item = DegreeItem()
        item['classes_num'] = 0
        item['chinaese_title'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="title"]/text()').extract_first(
            '暂无').replace('\r', '').replace('\t', '').replace('\n', '')
        list_info = response.xpath('//div[@class="left_con_top"]/ul//li/div[1]/text()').extract()
        # print(list_info)
        if '关键词：' in list_info:
            panten = re.compile('<div\sclass="info_left">关键词：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['chinaese_key'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '作者：' in list_info:
            panten = re.compile('<div\sclass="info_left">作者：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['chinaese_name'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                 '').replace(
                '\n', '')
        if '学位授予单位：' in list_info:
            panten = re.compile('<div\sclass="info_left">学位授予单位：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['degree_dw'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '授予学位：' in list_info:
            panten = re.compile('<div\sclass="info_left">授予学位：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['degree_dw'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '学科专业：' in list_info:
            panten = re.compile('<div\sclass="info_left">学科专业：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['degree_profession'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace(
                '\r', '').replace('\n', '')
        if '导师姓名：' in list_info:
            panten = re.compile('<div\sclass="info_left">导师姓名：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['teacher_name'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '学位年度：' in list_info:
            panten = re.compile('<div\sclass="info_left">学位年度：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['degree_year'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')
        if '语种：' in list_info:
            panten = re.compile('<div\sclass="info_left">语种：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
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
            item['create_time'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')

        yield item

    def prase_politics_data(self, response):
        item = DegreeItem()
        item['classes_num'] = 1
        item['chinaese_title'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="title"]/text()').extract_first(
            '暂无').replace('\r', '').replace('\t', '').replace('\n', '')
        list_info = response.xpath('//div[@class="left_con_top"]/ul//li/div[1]/text()').extract()
        # print(list_info)
        if '关键词：' in list_info:
            panten = re.compile('<div\sclass="info_left">关键词：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['chinaese_key'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '作者：' in list_info:
            panten = re.compile('<div\sclass="info_left">作者：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['chinaese_name'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                 '').replace(
                '\n', '')
        if '学位授予单位：' in list_info:
            panten = re.compile('<div\sclass="info_left">学位授予单位：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['degree_dw'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '授予学位：' in list_info:
            panten = re.compile('<div\sclass="info_left">授予学位：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['degree_dw'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '学科专业：' in list_info:
            panten = re.compile('<div\sclass="info_left">学科专业：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['degree_profession'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace(
                '\r', '').replace('\n', '')
        if '导师姓名：' in list_info:
            panten = re.compile('<div\sclass="info_left">导师姓名：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['teacher_name'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '学位年度：' in list_info:
            panten = re.compile('<div\sclass="info_left">学位年度：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['degree_year'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')
        if '语种：' in list_info:
            panten = re.compile('<div\sclass="info_left">语种：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
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
            item['create_time'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')

        yield item
