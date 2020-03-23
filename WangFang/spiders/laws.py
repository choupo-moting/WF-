# -*- coding: utf-8 -*-
import scrapy, re
from lxml.html import etree
from WangFang.items import LawsItem
from scrapy_redis.spiders import RedisCrawlSpider


class LawsSpider(scrapy.Spider):
    # class LawsSpider(RedisCrawlSpider):
    name = 'laws'
    allowed_domains = ['wanfangdata.com.cn']
    start_urls = ['http://s.wanfangdata.com.cn/Claw.aspx?q=%E6%94%BF%E6%B2%BB&f=top&p=1',  # zz
                  'http://s.wanfangdata.com.cn/Claw.aspx?q=%E6%B3%95%E5%BE%8B&f=top&p=1']  # falv

    # redis_key = 'laws:start_urls'
    def parse(self, response):
        if response:

            if '%E6%B3%95%E5%BE%8B' in response.url:  # 法律
                ID_list = response.xpath('.//div[@class="record-item-list"]/div[@class="record-item"]')
                print(ID_list)
                for ID in ID_list:
                    # 从原版的详情的url上获取详情ID，然后拼接  print(id)
                    id = (ID.xpath('.//div[@class="record-title"]/a[@class="title"]/@href').extract_first('').split('/'))[-1]

                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=legislations&id={}'.format(id)
                    # print(newurl)
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.parse_laws_data
                    )
                    # print('1111111111111111111111111111111111111111111')

                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//p[@class="pager"]/a').extract()) > 4:
                #                 #     print(len(response.xpath('.//p[@class="pager"]/a').extract()),
                #                 #           '=================')
                next_url = 'http://s.wanfangdata.com.cn/Claw.aspx?q=%E6%B3%95%E5%BE%8B&f=top&p={}'.format(
                    int(page) + 1)
                print(
                    '===================================================开始爬取法规下法律第{}页================================================================='.format(
                        page))

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
                # else:
                #     print('法规下法律数据爬取完毕！')
            if '%E6%94%BF%E6%B2%BB' in response.url:  # 政治
                ID_list = response.xpath('.//div[@class="record-item-list"]/div[@class="record-item"]')
                for ID in ID_list:
                    # 从原版的详情的url上获取详情ID，然后拼接
                    id = \
                    (ID.xpath('.//div[@class="record-title"]/a[@class="title"]/@href').extract_first('').split('/'))[-1]
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=legislations&id={}'.format(id)
                    print(newurl)
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.parse_zhengzhi_data
                    )
                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//p[@class="pager"]/a').extract()) > 4:
                #     print(len(response.xpath('.//p[@class="pager"]/a').extract()),
                #           '=================')
                next_url = 'http://s.wanfangdata.com.cn/Claw.aspx?q=%E6%94%BF%E6%B2%BB&f=top&p={}'.format(
                    int(page) + 1)
                print(
                    '===================================================开始爬取法规下政治第{}页================================================================='.format(
                        page))

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
                # else:
                #     print('法规下政治数据爬取完毕！')

    def parse_laws_data(self, response):
        """
         #hao
        classes_num = scrapy.Field()
        #中文标题
        chinese_title = scrapy.Field()
        #库别名称
        base_name = scrapy.Field()
        #颁布部门 
        issu_department = scrapy.Field()
        #效力级别
        level = scrapy.Field()
        #时效性
        timeliness = scrapy.Field()
        #颁布日期
        issu_date = scrapy.Field()
        #实施日期
        doit_date=scrapy.Field()
        #内容分类
        content_classes = scrapy.Field()

        :param response:
        :return:
        """
        item = LawsItem()
        item['classes_num'] = 0
        item['chinese_title'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r', '').replace(
            '\t', '').replace('\n', '')
        list_info = response.xpath('//div[@class="left_con_top"]/ul//li/div[1]/text()').extract()
        print(list_info)
        if '库别名称：' in list_info:
            panten = re.compile('<div\sclass="info_left">库别名称：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['base_name'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '颁布部门：' in list_info:
            panten = re.compile('<div\sclass="info_left">颁布部门：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['issu_department'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                   '').replace(
                '\n', '')
        if '效力级别：' in list_info:
            panten = re.compile('<div\sclass="info_left">效力级别：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['level'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                         '').replace(
                '\n', '')
        if '时效性：' in list_info:
            panten = re.compile('<div\sclass="info_left">时效性：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['timeliness'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                              '').replace(
                '\n', '')
        if '颁布日期：' in list_info:
            panten = re.compile('<div\sclass="info_left">颁布日期：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['issu_date'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '实施日期：' in list_info:
            panten = re.compile('<div\sclass="info_left">实施日期：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['doit_date'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '内容分类：' in list_info:
            panten = re.compile('<div\sclass="info_left">内容分类：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['content_classes'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                   '').replace(
                '\n', '')

        yield item

    def parse_zhengzhi_data(self, response):
        item = LawsItem()
        item['classes_num'] = 1
        item['chinese_title'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r', '').replace(
            '\t', '').replace('\n', '')
        list_info = response.xpath('//div[@class="left_con_top"]/ul//li/div[1]/text()').extract()
        print(list_info)
        if '库别名称：' in list_info:
            panten = re.compile('<div\sclass="info_left">库别名称：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['base_name'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '颁布部门：' in list_info:
            panten = re.compile('<div\sclass="info_left">颁布部门：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['issu_department'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                   '').replace(
                '\n', '')
        if '效力级别：' in list_info:
            panten = re.compile('<div\sclass="info_left">效力级别：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['level'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                         '').replace(
                '\n', '')
        if '时效性：' in list_info:
            panten = re.compile('<div\sclass="info_left">时效性：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['timeliness'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                              '').replace(
                '\n', '')
        if '颁布日期：' in list_info:
            panten = re.compile('<div\sclass="info_left">颁布日期：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['issu_date'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '实施日期：' in list_info:
            panten = re.compile('<div\sclass="info_left">实施日期：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['doit_date'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '内容分类：' in list_info:
            panten = re.compile('<div\sclass="info_left">内容分类：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['content_classes'] = ','.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                   '').replace(
                '\n', '')

        yield item
