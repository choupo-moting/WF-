# -*- coding: utf-8 -*-
"""主爬虫文件"""
from scrapy.crawler import CrawlerProcess
import scrapy,json


class WfangSpider(scrapy.Spider):
    name = 'wfang'
    allowed_domains = ['wanfangdata.com.cn']
    start_urls = ['http://old.wanfangdata.com.cn/']

    def parse(self, response):
        from .degree import DegreeSpider
        from .kanqi import KanqiSpider
        from .laws import LawsSpider
        from .meeting import MeetingSpider
        from .scientific_report import ScientificReportSpider
        from .patent import PatentSpider
        process = CrawlerProcess()
        process.crawl(DegreeSpider)
        process.crawl(KanqiSpider)
        process.crawl(LawsSpider)
        process.crawl(MeetingSpider)
        process.crawl(ScientificReportSpider)
        process.crawl(PatentSpider)
        process.start()


