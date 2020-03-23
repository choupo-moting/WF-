# -*- coding: utf-8 -*-
import scrapy, re
from WangFang.items import PatentItem
from lxml.html import etree
from scrapy_redis.spiders import RedisCrawlSpider


# class PatentSpider(RedisCrawlSpider):
class PatentSpider(scrapy.Spider):
    name = 'patent'
    allowed_domains = ['wanfangdata.com.cn']
    start_urls = ['http://s.wanfangdata.com.cn/patent.aspx?q=%E6%B3%95%E5%BE%8B&f=top&p=1',
                  'http://s.wanfangdata.com.cn/patent.aspx?q=%E6%94%BF%E6%B2%BB&F=top&p=1']

    # redis_key = 'patent:start_urls'

    # old法律http://s.wanfangdata.com.cn/patent.aspx?q=%E6%B3%95%E5%BE%8B&f=top
    # old政治http://s. .com.cn/patent.aspx?q=%E6%94%BF%E6%B2%BB&f=top
    # new detail http://www.wanfangdata.com.cn/details/detail.do?_type=patent&id=CN201711372221.1
    def parse(self, response):
        if response:
            if '%E6%B3%95%E5%BE%8B' in response.url:
                ID_list = response.xpath('//div[@class="record-item-list"]/div')
                for ID in ID_list:
                    id = ID.xpath('.//a[@class="fulltext"]/@href').extract_first().split('_')[-1]
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=patent&id=' + id
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.parse_laws_data
                    )

                # page_num = 1686#int(response.xpath(
                #     # '//div[@class="record-item-list"]/p[@class="pager"]/span[@class="page_link"]/text()').extract_first().split(
                #     # '/')[1])
                # page = int(re.search('\d+$', response.url).group())
                # if page_num >= page:
                #     next_page = 'http://s.wanfangdata.com.cn/patent.aspx?q=%E6%B3%95%E5%BE%8B&f=top&p={}'.format(
                #         page + 1)
                #     yield scrapy.Request(
                #         url=next_page,
                #         callback=self.parse
                #     )
                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()) > 4:
                #     print(len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()),
                #           '=================')
                next_url = 'http://s.wanfangdata.com.cn/patent.aspx?q=%E6%B3%95%E5%BE%8B&f=top&p={}'.format(
                    int(page) + 1)
                print('开始爬取专利下法律第{}页================================================================='.format(
                    int(page) + 1))

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
                # else:
                #     print('获取专利下法律完毕')
            if '%E6%94%BF%E6%B2%BB' in response.url:
                ID_list = response.xpath('//div[@class="record-item-list"]/div')
                for ID in ID_list:
                    id = ID.xpath('.//a[@class="fulltext"]/@href').extract_first().split('_')[-1]
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=patent&id=' + id
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.parse_politics_data
                    )

                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()) > 4:
                #     print(len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()),
                #           '=================')
                next_url = 'http://s.wanfangdata.com.cn/patent.aspx?q=%E6%94%BF%E6%B2%BB&f=top&p={}'.format(
                    int(page) + 1)
                print('开始爬取专利下政治第{}页================================================================='.format(
                    int(page) + 1))

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
                # else:
                #     print('获取专利下政治完毕')

    def parse_laws_data(self, response):
        """
         #类型号
        classes_num = scrapy.Field()
        #中文名称
        chinese_name = scrapy.Field()
        #摘要
        doi_text = scrapy.Field()
        #专利类型
        classes = scrapy.Field()
        #申请/专利号
        apply_for_mark = scrapy.Field()
        #申请日期
        apply_for_date = scrapy.Field()
        #公开/公告号
        public_mark = scrapy.Field()
        #主分类号
        pirmary_mark = scrapy.Field()
        #申请/专利权人
        proposer = scrapy.Field()
        #发明/设计人
        designer = scrapy.Field()
        #主申请人地址
        address = scrapy.Field()
        #专利代理机构
        organization = scrapy.Field()
        #代理人
        agent = scrapy.Field()
        #国别省市代码
        mark = scrapy.Field()
        #法律状态
        law_staut = scrapy.Field()
        :param response:
        :return:
        """
        print(response.url, '=-=-=-=-=-=-=-=-=-=-=-=')
        item = PatentItem()
        item['classes_num'] = 0
        item['chinese_name'] = response.xpath(
            '//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first().replace('\t', '').replace('\r',
                                                                                                                 '').replace(
            '\n', '').replace('  ', '')
        item['doi_text'] = response.xpath('//div[@id="see_alldiv"]/text()').extract_first().replace('\t', '')
        list_info = response.xpath('//div[@class="left_con_top"]/ul/li/div[1]/text()').extract()
        # print(list_info)
        if '专利类型：' in list_info:
            panten = re.compile('<div\sclass="info_left">专利类型：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['classes'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                           '').replace(
                '\n', '')

        if '申请/专利号：' in list_info:
            panten = re.compile('<div\sclass="info_left">申请/专利号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['apply_for_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                  '').replace(
                '\n', '')

        if '申请日期：' in list_info:
            panten = re.compile('<div\sclass="info_left">申请日期：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['apply_for_date'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                  '').replace(
                '\n', '')

        if '公开/公告号：' in list_info:
            panten = re.compile('<div\sclass="info_left">公开/公告号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['public_mark'] = ' '.join(dssss.xpath('//text()')).replace('\
            t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')
        if '主分类号：' in list_info:
            panten = re.compile('<div\sclass="info_left">主分类号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['pirmary_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '申请/专利权人：' in list_info:
            panten = re.compile('<div\sclass="info_left">申请/专利权人：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['proposer'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                            '').replace(
                '\n', '')
        if '发明/设计人：' in list_info:
            panten = re.compile('<div\sclass="info_left">发明/设计人：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['designer'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                            '').replace(
                '\n', '')

        if '主申请人地址：' in list_info:
            panten = re.compile('<div\sclass="info_left">主申请人地址：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['address'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                           '').replace(
                '\n', '')

        if '专利代理机构：' in list_info:
            panten = re.compile('<div\sclass="info_left">专利代理机构：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['organization'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '代理人：' in list_info:
            panten = re.compile('<div\sclass="info_left">代理人：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])

            item['agent'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                         '').replace(
                '\n', '')

        if '国别省市代码：' in list_info:
            panten = re.compile('<div\sclass="info_left">国别省市代码：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                        '').replace(
                '\n', '')
        if '法律状态：' in list_info:
            panten = re.compile('<div\sclass="info_left">法律状态：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['law_staut'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')

        yield item

    def parse_politics_data(self, response):

        print(response.url, '=-=-=-=-=-=-=-=-=-=-=-=')
        item = PatentItem()
        item['classes_num'] = 1
        item['chinese_name'] = response.xpath(
            '//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first().replace('\t', '').replace('\r',
                                                                                                                 '').replace(
            '\n', '').replace('  ', '')
        item['doi_text'] = response.xpath('//div[@id="see_alldiv"]/text()').extract_first().replace('\t', '')
        list_info = response.xpath('//div[@class="left_con_top"]/ul/li/div[1]/text()').extract()
        # print(list_info)
        if '专利类型：' in list_info:
            panten = re.compile('<div\sclass="info_left">专利类型：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['classes'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                           '').replace(
                '\n', '')

        if '申请/专利号：' in list_info:
            panten = re.compile('<div\sclass="info_left">申请/专利号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['apply_for_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                  '').replace(
                '\n', '')

        if '申请日期：' in list_info:
            panten = re.compile('<div\sclass="info_left">申请日期：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['apply_for_date'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                  '').replace(
                '\n', '')

        if '公开/公告号：' in list_info:
            panten = re.compile('<div\sclass="info_left">公开/公告号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['public_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')
        if '主分类号：' in list_info:
            panten = re.compile('<div\sclass="info_left">主分类号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['pirmary_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '申请/专利权人：' in list_info:
            panten = re.compile('<div\sclass="info_left">申请/专利权人：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['proposer'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                            '').replace(
                '\n', '')
        if '发明/设计人：' in list_info:
            panten = re.compile('<div\sclass="info_left">发明/设计人：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['designer'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                            '').replace(
                '\n', '')

        if '主申请人地址：' in list_info:
            panten = re.compile('<div\sclass="info_left">主申请人地址：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['address'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                           '').replace(
                '\n', '')

        if '专利代理机构：' in list_info:
            panten = re.compile('<div\sclass="info_left">专利代理机构：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['organization'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '代理人：' in list_info:
            panten = re.compile('<div\sclass="info_left">代理人：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])

            item['agent'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                         '').replace(
                '\n', '')

        if '国别省市代码：' in list_info:
            panten = re.compile('<div\sclass="info_left">国别省市代码：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                        '').replace(
                '\n', '')
        if '法律状态：' in list_info:
            panten = re.compile('<div\sclass="info_left">法律状态：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['law_staut'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')

        yield item
