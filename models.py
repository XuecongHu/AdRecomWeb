# -*- coding:utf-8 -*-
__author__ = 'frank'
from flask_table import Table, Col

# 定义表格类
class ItemTable(Table):
    user_name = Col(u"常去频道")
    goods = Col(u"推荐商品类")


# 定义表格元素类
class Item(object):
    def __init__(self, user_name, goods):
        self.user_name = user_name
        self.goods = goods
