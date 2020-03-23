# -*- coding: utf-8 -*-
import scrapy, re
from lxml.html import etree
from WangFang.items import ScientificReportItem
from scrapy_redis.spiders import RedisCrawlSpider


class ScientificReportSpider(scrapy.Spider):
    # class ScientificReportSpider(RedisCrawlSpider):
    name = 'scientific_report'
    allowed_domains = ['wanfangdata.com.cn']
    start_urls = ['http://s.wanfangdata.com.cn/NSTR.aspx?q=%E6%B3%95%E5%BE%8B&f=top&p=1',  # 法律
                  'http://s.wanfangdata.com.cn/NSTR.aspx?q=%E6%94%BF%E6%B2%BB&f=top&p=1']  # zz

    # redis_key = 'scientific_report:start_urls'
    def parse(self, response):
        if response:

            if '%E6%B3%95%E5%BE%8B' in response.url:  # 法律
                ID_list = response.xpath('.//div[@class="record-item-list"]/div[@class="record-item"]')
                for ID in ID_list:
                    # 从原版的详情的url上获取详情ID，然后拼接
                    id = \
                        (ID.xpath('.//div[@class="record-title"]/a[@class="title"]/@href').extract_first('').split(
                            '/'))[-1]
                    print(id)
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=tech&id={}'.format(id)
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.parse_laws_data
                    )
                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//p[@class="pager"]/a').extract()) > 2:
                # print(len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()),
                #       '=================')
                if not response.xpath('//div[@class="empty"]/span[@class="msg"]/text()'):
                    next_url = 'http://s.wanfangdata.com.cn/NSTR.aspx?q=%E6%B3%95%E5%BE%8B&f=top&p={}'.format(
                        int(page) + 1)
                    print(
                        '开始爬取科学技术下法律第{}页================================================================='.format(page))

                    yield scrapy.Request(
                        url=next_url,
                        callback=self.parse
                    )
                else:
                    print('学科法律数据爬取完毕！')

            if '%E6%94%BF%E6%B2%BB' in response.url:  # 政治
                ID_list = response.xpath('.//div[@class="record-item-list"]/div[@class="record-item"]')
                for ID in ID_list:
                    # 从原版的详情的url上获取详情ID，然后拼接
                    id = \
                        (ID.xpath('.//div[@class="record-title"]/a[@class="title"]/@href').extract_first('').split(
                            '/'))[-1]
                    print(id)
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=tech&id={}'.format(id)
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.parse_zhengzhi_data
                    )
                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//p[@class="pager"]/a').extract()) > 2:
                #     print(len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()),
                #           '=================')
                if not response.xpath('//div[@class="empty"]/span[@class="msg"]/text()'):
                    next_url = 'http://s.wanfangdata.com.cn/NSTR.aspx?q=%E6%94%BF%E6%B2%BB&f=top&p={}'.format(
                        int(page) + 1)
                    print(
                        '开始爬取科学技术下政治第{}页================================================================='.format(page))

                    yield scrapy.Request(
                        url=next_url,
                        callback=self.parse
                    )
                else:
                    print('学科政治数据爬取完毕！')

    def parse_laws_data(self, response):
        """
        #hao
        classes_num=scrapy.Field()
        #中文标题
        chinese_title=scrapy.Field()
        #英文标题
        english_title = scrapy.Field()
        #摘要
        abstract = scrapy.Field()
        #中文关键语
        chinese_key = scrapy.Field()
        #作者中文名
        author_chinaese = scrapy.Field()
        #作者单位
        author_dw = scrapy.Field()
        #报告类型
        classes_report = scrapy.Field()
        #公开范围 
        public_scope = scrapy.Field()
        #全文页数
        all_page = scrapy.Field()
        #项目/课题名称
        project_name=scrapy.Field()
        #计划名称
        plan_name = scrapy.Field()
        #编制时间
        bianz_time = scrapy.Field()
        #立项批准年
        ratify_year = scrapy.Field()
        #馆藏号
        holding_mark = scrapy.Field()

        :param response:
        :return:
        """
        item = ScientificReportItem()
        item['classes_num'] = 0
        item['chinese_title'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r', '').replace(
            '\t', '').replace('\n', '')
        item['english_title'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="English"]/text()').extract_first('暂无').replace('\r', '').replace(
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
        if '报告类型：' in list_info:
            panten = re.compile('<div\sclass="info_left">报告类型：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['classes_report'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                  '').replace(
                '\n', '')
        if '公开范围：' in list_info:
            panten = re.compile('<div\sclass="info_left">公开范围：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['public_scope'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '全文页数：' in list_info:
            panten = re.compile('<div\sclass="info_left">全文页数：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['all_page'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                            '').replace(
                '\n', '')
        if '项目/课题名称：' in list_info:
            panten = re.compile('<div\sclass="info_left">项目/课题名称：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['project_name'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '计划名称：' in list_info:
            panten = re.compile('<div\sclass="info_left">计划名称：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['plan_name'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '编制时间：' in list_info:
            panten = re.compile('<div\sclass="info_left">编制时间：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['bianz_time'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                              '').replace(
                '\n', '')
        if '立项批准年：' in list_info:
            panten = re.compile('<div\sclass="info_left">立项批准年：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['ratify_year'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')
        if '馆藏号：' in list_info:
            panten = re.compile('<div\sclass="info_left">馆藏号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['holding_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        yield item

    def parse_zhengzhi_data(self, response):
        item = ScientificReportItem()
        item['classes_num'] = 1
        item['chinese_title'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r', '').replace(
            '\t', '').replace('\n', '')
        item['english_title'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="English"]/text()').extract_first('暂无').replace('\r', '').replace(
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
        if '报告类型：' in list_info:
            panten = re.compile('<div\sclass="info_left">报告类型：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['classes_report'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                  '').replace(
                '\n', '')
        if '公开范围：' in list_info:
            panten = re.compile('<div\sclass="info_left">公开范围：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['public_scope'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '全文页数：' in list_info:
            panten = re.compile('<div\sclass="info_left">全文页数：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['all_page'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                            '').replace(
                '\n', '')
        if '项目/课题名称：' in list_info:
            panten = re.compile('<div\sclass="info_left">项目/课题名称：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['project_name'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        if '计划名称：' in list_info:
            panten = re.compile('<div\sclass="info_left">计划名称：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['plan_name'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                             '').replace(
                '\n', '')
        if '编制时间：' in list_info:
            panten = re.compile('<div\sclass="info_left">编制时间：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['bianz_time'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                              '').replace(
                '\n', '')
        if '立项批准年：' in list_info:
            panten = re.compile('<div\sclass="info_left">立项批准年：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['ratify_year'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                               '').replace(
                '\n', '')
        if '馆藏号：' in list_info:
            panten = re.compile('<div\sclass="info_left">馆藏号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['holding_mark'] = ' '.join(dssss.xpath('//text()')).replace('\t', '').replace(' ', '').replace('\r',
                                                                                                                '').replace(
                '\n', '')
        yield item
