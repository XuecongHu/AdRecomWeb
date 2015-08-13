# -*- coding:utf-8 -*-
__author__ = 'frank'
from flask_table import Table, Col

# 定义商品表格类
class GoodsTable(Table):
    freq = Col(u"序号")
    user_name = Col(u"常去频道top5之内")
    goods = Col(u"推荐商品类")
    counts = Col(u"频数")


# 定义商品表格元素类
class GoodsItem(object):
    def __init__(self, freq, user_name, goods, counts):
        self.user_name = user_name
        self.goods = goods
        self.freq = freq
        self.counts = counts

# 定义相似用户表格类
class SimUserTable(Table):
    user_id = Col(u"相似用户ID top5之内")

class SimUserTtem(object):
    def __init__(self, user_id):
        self.user_id = user_id