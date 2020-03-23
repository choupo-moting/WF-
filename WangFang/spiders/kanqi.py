# -*- coding: utf-8 -*-
import scrapy, urllib, re
from WangFang.items import KanqiItem
from lxml.html import etree
from scrapy_redis.spiders import RedisCrawlSpider


# class KanqiSpider(RedisCrawlSpider):
class KanqiSpider(scrapy.Spider):
    name = 'kanqi'
    allowed_domains = ['wanfangdata.com.cn']
    start_urls = ['http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%94%BF%E6%B2%BB%20DBID%3AWF_QK&f=top&p=1',
                  'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3AWF_QK&f=top&p=1']
    # redis_key = 'kanqi:start_urls'

    def parse(self, response):
        if response:
            if '%E6%B3%95%E5%BE%8B' in response.url:  # 法律
                ID_list = response.xpath('.//div[@class="record-item-list"]/div[@class="record-item"]')
                for ID in ID_list:
                    # 从原版的详情的url上获取详情ID，然后拼接
                    id = \
                        (ID.xpath('.//div[@class="record-title"]/a[@class="title"]/@href').extract_first('').split(
                            '/'))[-1]
                    # http: // www.wanfangdata.com.cn / details / detail.do?_type = perio & id = ystmzwhxk201904015
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id={}'.format(id)
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.parse_laws_data
                    )
                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()) > 4:
                #     print(len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()),
                #           '=================')
                next_url = 'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%B3%95%E5%BE%8B%20DBID%3aWF_QK&f=top&p={}'.format(
                    int(page) + 1)
                print('开始爬取刊期下法律第{}页================================================================='.format(
                    int(page) + 1))

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
                # else:
                #     print('爬取刊期下法律爬取完毕')
            if '%E6%94%BF%E6%B2%BB' in response.url:
                ID_list = response.xpath('.//div[@class="record-item-list"]/div[@class="record-item"]')
                for ID in ID_list:
                    # 从原版的详情的url上获取详情ID，然后拼接
                    id = \
                        (ID.xpath('.//div[@class="record-title"]/a[@class="title"]/@href').extract_first('').split(
                            '/'))[-1]
                    # http: // www.wanfangdata.com.cn / details / detail.do?_type = perio & id = ystmzwhxk201904015
                    newurl = 'http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id={}'.format(id)
                    yield scrapy.Request(
                        url=newurl,
                        callback=self.prase_politics_data
                    )
                page = re.search('\d+$', response.url).group()
                # if len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()) > 4:
                #     print(len(response.xpath('.//div[@class="record-item-list"]/p[@class="pager"]/a').extract()),
                #           '=================')
                next_url = 'http://s.wanfangdata.com.cn/Paper.aspx?q=%E6%94%BF%E6%B2%BB%20DBID%3AWF_QK&f=top&p={}'.format(
                    int(page) + 1)
                print('开始爬取刊期下政治第{}页================================================================='.format(
                    int(page) + 1))

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
                # else:
                #     print('刊期下政治爬取完毕')

    def parse_laws_data(self, response):
        print(response.url, '===========')
        item = KanqiItem()
        """
        # 类别
        type_num = scrapy.Field()
        # 中文标题
        chinase_name = scrapy.Field()
        # 英文标题
        english_name = scrapy.Field()
        # 摘要
        zyao_text = scrapy.Field()
        # doi
        doi_text = scrapy.Field()
        # 中文关键字
        chinase_key = scrapy.Field()
        # 英文关键词
        english_key = scrapy.Field()
        # 作者中文名
        author_chinase = scrapy.Field()
        # 作者英文名
        author_english = scrapy.Field()
        # 作者单位
        author_dw = scrapy.Field()
        # 刊名
        k_name = scrapy.Field()
        # Journal
        Journal = scrapy.Field()
        # 年，卷（期）
        yaer_qo = scrapy.Field()
        # 所属期刊栏目
        ssqkklm = scrapy.Field()
        # 分类号
        classes_num = scrapy.Field()
        # 基金项目
        fund_program = scrapy.Field()
        # 出版日期 
        create_date = scrapy.Field()
        # 页数
        page_data = scrapy.Field()
        # 页码
        page_num = scrapy.Field()
        """
        item['type_num'] = 0
        item['chinase_name'] = response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first(
            '暂无').replace('\r', '').replace('\t', '').replace('\n', '')
        item['english_name'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="English"]/text()').extract_first('暂无').replace('\r', '').replace(
            '\t', '').replace('\n', '')
        item['zyao_text'] = response.xpath('.//div[@id="see_alldiv"]/text()').extract_first('暂无').replace('\r',
                                                                                                          '').replace(
            '\t', '').replace('\n', '')
        list_info = response.xpath('//div[@class="left_con_top"]/ul//li/div[1]/text()').extract()
        print(list_info)
        if 'doi：' in list_info:
            index = list_info.index('doi：') + 1
            item['doi_text'] = response.xpath(
                '//div[@class="left_con_top"]/ul/li[{}]/div[2]/a/text()'.format(index)).extract_first('')
        if '关键词：' in list_info:
            index = list_info.index('关键词：') + 1
            item['chinase_key'] = ','.join(
                response.xpath('//div[@class="left_con_top"]/ul/li[{}]/div[2]/a/text()'.format(index)).extract())
        if 'Keyword：' in list_info:
            index = list_info.index('Keyword：') + 1
            item['english_key'] = ','.join(
                response.xpath('//div[@class="left_con_top"]/ul/li[{}]/div[2]/a/text()'.format(index)).extract())
        if '作者：' in list_info:
            index = list_info.index('作者：') + 1
            item['author_chinase'] = ','.join(
                response.xpath('//div[@class="left_con_top"]/ul/li[{}]/div[2]/a/text()'.format(index)).extract())
        if 'Author：' in list_info:
            panten = re.compile('<div\sclass="info_left">Author：</div>.*?<div\sclass="info_right">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['author_english'] = ''.join(dssss.xpath('//text()')).replace('\r\n\t\t\t\t', '').replace('作者单位：',
                                                                                                          '').replace(
                '\r\n\t\t\t\r\n\t', '')

        if '作者单位：' in list_info:
            panten = re.compile('<div\sclass="info_left">作者单位：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['author_dw'] = ''.join(dssss.xpath('//text()')).replace('\r\n\t\t\t\t\t', '')

        if '刊名：' in list_info:
            panten = re.compile('<div\sclass="info_left">刊名：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['k_name'] = dssss.xpath('//text()')[0]
        if 'Journal：' in list_info:
            panten = re.compile('<div\sclass="info_left">Journal：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['Journal'] = dssss.xpath('//text()')[0]
        if '年，卷(期)：' in list_info:
            panten = re.compile('<div\sclass="info_left">年，卷\(期\)：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['yaer_qo'] = dssss.xpath('//text()')[0]
        if '所属期刊栏目：' in list_info:
            panten = re.compile('<div\sclass="info_left">所属期刊栏目：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['ssqkklm'] = dssss.xpath('//text()')[0]
        if '分类号：' in list_info:
            panten = re.compile('<div\sclass="info_left">分类号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['classes_num'] = dssss.xpath('//text()')[0]
        if '基金项目：' in list_info:
            panten = re.compile('<div\sclass="info_left">基金项目：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['fund_program'] = dssss.xpath('//text()')[0]
        if '在线出版日期：' in list_info:
            panten = re.compile('<div\sclass="info_left">在线出版日期：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['create_date'] = dssss.xpath('//text()')[0]
        if '页数：' in list_info:
            panten = re.compile('<div\sclass="info_left">页数：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['page_data'] = dssss.xpath('//text()')[0]
        if '页码：' in list_info:
            panten = re.compile('<div\sclass="info_left">页码：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['page_num'] = dssss.xpath('//text()')[0]
        # for iten in (response.css('div.left_con_top ul.info li:nth-child(5) div:nth-child(2) a#card0').extract()):
        #     print(iten)
        # for iten in (response.css('div.left_con_top ul.info li:nth-child(5) div:nth-child(2) a#card1').extract()):
        #     print(iten)
        # print([item for item in response.xpath('//div[@class="left_con_top"]/ul/li').extract()],'===================================================')
        # with open('page.html', 'w', encoding='utf8') as file:
        #     file.write(str(response.xpath('//div[@class="left_con_top"]/ul/li').extract()))
        # for info in response.xpath('//div[@class="left_con_top"]/ul/li'):
        #     print(response.xpath('//div[@class="left_con_top"]/ul/li'))
        #
        #     if info.xpath('./div[1]/text()').extract() == 'doi：':
        #         item['doi_text'] = info.xpath('./div[2]/a/text()').extract_first('')
        #     if info.xpath('./div[1]/text()').extract() == '关键词：':

        #         item['chinase_key'] =','.join(info.xpath('./div[2]/a/t
        #         ext()').extract())
        #     if info.xpath('./div[1]/text()').extract() == 'Keyword：':
        #         item['english_key'] =','.join(info.xpath('./div[2]/a/text()').extract())
        #     if info.xpath('./div[1]/text()').extract_first('') == '作者：':
        #         item['author_chinase'] =','.join(info.xpath('./div[2]/a/text()').extract())
        #     if info.xpath('./div[1]/text()').extract_first('') == 'Author：':
        #         item['author_english'] =','.join(info.xpath('./div[2]/a/text()').extract())
        #     if info.xpath('./div[1]/text()').extract_first('') == '作者单位：':
        #         item['author_dw'] =','.join(info.xpath('./div[2]/a/text()').extract())
        #     if info.xpath('./div[1]/text()').extract_first('') == '刊名：':
        #         item['k_name'] =','.join(info.xpath('./div[2]/a/text()').extract())
        #     if info.xpath('./div[1]/text()').extract_first('') == 'Journal：':
        #         item['Journal'] =','.join(info.xpath('./div[2]/a/text()').extract())
        #     if info.xpath('./div[1]/text()').extract_first('') == '年，卷(期)：':
        #         item['yaer_qo'] =','.join(info.xpath('./div[2]/a/text()').extract())
        #     if info.xpath('./div[1]/text()').extract_first('') == '所属期刊栏目：':
        #         item['ssqkklm'] =','.join(info.xpath('./div[2]/a/text()').extract())
        #     if info.xpath('./div[1]/text()').extract_first('') == '分类号：':
        #         item['classes_num'] =info.xpath('./div[2]/a/text()').extract_first('')
        #     if info.xpath('./div[1]/text()').extract_first('') == '基金项目：':
        #         item['fund_program'] =','.join(info.xpath('./div[2]/a/text()').extract())
        #     if info.xpath('./div[1]/text()').extract_first('') == '在线出版日期：':
        #        item['create_date'] =','.join(info.xpath('./div[2]/a/text()').extract())
        #     if info.xpath('./div[1]/text()').extract_first('') == '页数：':
        #         item['page_data'] =info.xpath('./div[2]/a/text()').extract_first('')
        #     if info.xpath('./div[1]/text()').extract_first('') == '页码：':
        #         item['page_num'] =info.xpath('./div[2]/a/text()').extract_first('')
        # item['doi_text']=response.xpath('.//div[@class="left_con_top"]/ul/li[1]/div[@class="info_right author"]/a/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['chinase_key']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['english_key']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['author_chinase']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['author_english']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['author_dw']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['k_name']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['Journal']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['yaer_qo']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['ssqkklm']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['classes_num']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['fund_program']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['create_date']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['page_data']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        # item['page_num']=response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first('暂无').replace('\r','').replace('\t','').replace('\n','')
        yield item

    def prase_politics_data(self, response):
        item = KanqiItem()
        """
        # 类别
        type_num = scrapy.Field()
        # 中文标题
        chinase_name = scrapy.Field()
        # 英文标题
        english_name = scrapy.Field()
        # 摘要
        zyao_text = scrapy.Field()
        # doi
        doi_text = scrapy.Field()
        # 中文关键字
        chinase_key = scrapy.Field()
        # 英文关键词
        english_key = scrapy.Field()
        # 作者中文名
        author_chinase = scrapy.Field()
        # 作者英文名
        author_english = scrapy.Field()
        # 作者单位
        author_dw = scrapy.Field()
        # 刊名
        k_name = scrapy.Field()
        # Journal
        Journal = scrapy.Field()
        # 年，卷（期）
        yaer_qo = scrapy.Field()
        # 所属期刊栏目
        ssqkklm = scrapy.Field()
        # 分类号
        classes_num = scrapy.Field()
        # 基金项目
        fund_program = scrapy.Field()
        # 出版日期 
        create_date = scrapy.Field()
        # 页数
        page_data = scrapy.Field()
        # 页码
        page_num = scrapy.Field()
        """
        item['type_num'] = 1
        item['chinase_name'] = response.xpath('.//div[@class="left_con_top"]/div[@class="title"]/text()').extract_first(
            '暂无').replace('\r', '').replace('\t', '').replace('\n', '')
        item['english_name'] = response.xpath(
            './/div[@class="left_con_top"]/div[@class="English"]/text()').extract_first('暂无').replace('\r', '').replace(
            '\t', '').replace('\n', '')
        item['zyao_text'] = response.xpath('.//div[@id="see_alldiv"]/text()').extract_first('暂无').replace('\r',
                                                                                                          '').replace(
            '\t', '').replace('\n', '')
        list_info = response.xpath('//div[@class="left_con_top"]/ul//li/div[1]/text()').extract()
        print(list_info)
        if 'doi：' in list_info:
            index = list_info.index('doi：') + 1
            item['doi_text'] = response.xpath(
                '//div[@class="left_con_top"]/ul/li[{}]/div[2]/a/text()'.format(index)).extract_first('')
        if '关键词：' in list_info:
            index = list_info.index('关键词：') + 1
            item['chinase_key'] = ','.join(
                response.xpath('//div[@class="left_con_top"]/ul/li[{}]/div[2]/a/text()'.format(index)).extract())
        if 'Keyword：' in list_info:
            index = list_info.index('Keyword：') + 1
            item['english_key'] = ','.join(
                response.xpath('//div[@class="left_con_top"]/ul/li[{}]/div[2]/a/text()'.format(index)).extract())
        if '作者：' in list_info:
            index = list_info.index('作者：') + 1
            item['author_chinase'] = ','.join(
                response.xpath('//div[@class="left_con_top"]/ul/li[{}]/div[2]/a/text()'.format(index)).extract())
        if 'Author：' in list_info:
            panten = re.compile('<div\sclass="info_left">Author：</div>.*?<div\sclass="info_right">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['author_english'] = ''.join(dssss.xpath('//text()')).replace('\r\n\t\t\t\t', '').replace('作者单位：',
                                                                                                          '').replace(
                '\r\n\t\t\t\r\n\t', '')
        if '作者单位：' in list_info:
            panten = re.compile('<div\sclass="info_left">作者单位：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['author_dw'] = ''.join(dssss.xpath('//text()')).replace('\r\n\t\t\t\t\t', '')

        if '刊名：' in list_info:
            panten = re.compile('<div\sclass="info_left">刊名：</div>.*?<div\sclass="info_right.*?">(.*?)</div>', re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['k_name'] = dssss.xpath('//text()')[0]
        if 'Journal：' in list_info:
            panten = re.compile('<div\sclass="info_left">Journal：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['Journal'] = dssss.xpath('//text()')[0]
        if '年，卷(期)：' in list_info:
            panten = re.compile('<div\sclass="info_left">年，卷\(期\)：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['yaer_qo'] = dssss.xpath('//text()')[0]
        if '所属期刊栏目：' in list_info:
            panten = re.compile('<div\sclass="info_left">所属期刊栏目：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['ssqkklm'] = dssss.xpath('//text()')[0]
        if '分类号：' in list_info:
            panten = re.compile('<div\sclass="info_left">分类号：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['classes_num'] = dssss.xpath('//text()')[0]
        if '基金项目：' in list_info:
            panten = re.compile('<div\sclass="info_left">基金项目：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['fund_program'] = dssss.xpath('//text()')[0]
        if '在线出版日期：' in list_info:
            panten = re.compile('<div\sclass="info_left">在线出版日期：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['create_date'] = dssss.xpath('//text()')[0]
        if '页数：' in list_info:
            panten = re.compile('<div\sclass="info_left">页数：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['page_data'] = dssss.xpath('//text()')[0]
        if '页码：' in list_info:
            panten = re.compile('<div\sclass="info_left">页码：</div>.*?<div\sclass="info_right.*?">(.*?)</div>',
                                re.S)
            data = re.findall(panten, response.text)
            dssss = etree.HTML(data[0])
            item['page_num'] = dssss.xpath('//text()')[0]
        yield item
