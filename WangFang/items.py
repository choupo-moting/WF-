# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class KanqiItem(scrapy.Item):
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
    def get_sql_str(self,item):
        sql = """
            INSERT INTO kanqi(%s)
            VALUE  (%s)"""%(
            ','.join(item.keys()),
            ','.join(['%s'] * len(item))
        )
        return sql


class PatentItem(scrapy.Item):
    # 类型号
    classes_num = scrapy.Field()
    # 中文名称
    chinese_name = scrapy.Field()
    # 摘要
    doi_text = scrapy.Field()
    # 专利类型
    classes = scrapy.Field()
    # 申请/专利号
    apply_for_mark = scrapy.Field()
    # 申请日期
    apply_for_date = scrapy.Field()
    # 公开/公告号
    public_mark = scrapy.Field()
    # 主分类号
    pirmary_mark = scrapy.Field()
    # 申请/专利权人
    proposer = scrapy.Field()
    # 发明/设计人
    designer = scrapy.Field()
    # 主申请人地址
    address = scrapy.Field()
    # 专利代理机构
    organization = scrapy.Field()
    # 代理人
    agent = scrapy.Field()
    # 国别省市代码
    mark = scrapy.Field()
    # 法律状态
    law_staut = scrapy.Field()
    def get_sql_str(self,item):
        sql = """
            INSERT INTO zhuanli(%s)
            VALUE  (%s)"""%(
            ','.join(item.keys()),
            ','.join(['%s'] * len(item))
        )
        return sql


class DegreeItem(scrapy.Item):
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
    def get_sql_str(self,item):
        sql = """
            INSERT INTO degree(%s)
            VALUE  (%s)"""%(
            ','.join(item.keys()),
            ','.join(['%s'] * len(item))
        )
        return sql

class MeetingItem(scrapy.Item):
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
    def get_sql_str(self,item):
        sql = """
            INSERT INTO meeting(%s)
            VALUE  (%s)"""%(
            ','.join(item.keys()),
            ','.join(['%s'] * len(item))
        )
        return sql
class ScientificReportItem(scrapy.Item):
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
    def get_sql_str(self,item):
        sql = """
            INSERT INTO scientificreport(%s)
            VALUE  (%s)"""%(
            ','.join(item.keys()),
            ','.join(['%s'] * len(item))
        )
        return sql

class LawsItem(scrapy.Item):
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
    def get_sql_str(self,item):
        sql = """
            INSERT INTO laws(%s)
            VALUE  (%s)"""%(
            ','.join(item.keys()),
            ','.join(['%s'] * len(item))
        )
        return sql
