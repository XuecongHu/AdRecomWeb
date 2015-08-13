# -*- coding:utf-8 -*-
__author__ = 'frank'
from models import GoodsItem, SimUserTtem
from numpy import *
from utils import *

def simple_recom(cursor, user_id):
    cursor.execute("select theme_id, count from user_theme where user_id = '"+user_id+"' order by count desc")
    themes_list = cursor.fetchall()

    num = 5  # 默认推荐数目
    if len(themes_list) < num:  # 如果查询结果少于5，则为查询出来的结果个数
        num = len(themes_list)

    table_itmes = []
    for i in range(num):
        theme_id = themes_list[i][0]
        count = themes_list[i][1]

        cursor.execute("select name from themes where id='"+str(theme_id)+"'")
        theme = cursor.fetchone()[0]

        cursor.execute("select gc_id from themes_goodsClass where theme_id = '"+str(theme_id)+"'")
        gc_list = cursor.fetchall()  # 取出频道主题对应的gc_id
        if len(gc_list) > 0:  # 频道主题对应有商品
            for gc in gc_list:
                gc_id = gc[0]
                cursor.execute("select name from goods_class where id = '"+str(gc_id)+"'")
                gc = cursor.fetchone()[0]
                table_itmes.append(GoodsItem(i+1, theme, gc, count))
        else:
            table_itmes.append(GoodsItem(i+1, theme, u"暂无数据", count))

    return table_itmes

def find_user_name(cursor, user_id):
    cursor.execute("select userName from user where userId='"+user_id+"'")
    user_name = cursor.fetchone()[0]
    return user_name


def find_similar_users(cursor, user_id):
    cursor.execute("select id from themes")
    themes = cursor.fetchall()

    theme_dict = {}
    index = 0
    for theme in themes:  # 创建一个频道主题名称及位置的map,方便以后构造每个用户的向量时
        theme_id = theme[0]
        theme_dict[theme_id] = index
        index += 1

    # 构造要查询的用户向量
    cursor.execute("select theme_id,count from user_theme where user_id='"+user_id+"'")
    user_info = cursor.fetchall()

    vec_len = len(themes)
    user_vec = zeros(vec_len)
    for item in user_info:
        theme_id = item[0]
        count = item[1]

        pos = theme_dict.get(theme_id)
        if pos is not None:
            user_vec[pos] = count

    cursor.execute("select userId from user")
    all_users = cursor.fetchall()

    simi_nums = 5
    simi_users = []  # （userId,value)
    for i in range(simi_nums):
        simi_users.append([-1, -1])

    # 对每个用户进行遍历，构造每个用户的向量
    for user in all_users:
        tuser_id = user[0]

        if tuser_id != user_id:
            tvec = zeros(vec_len)
            cursor.execute("select theme_id,count from user_theme where user_id='"+tuser_id+"'")
            tuser_info = cursor.fetchall()

            for info in tuser_info:
                theme_id = info[0]
                count = info[1]

                pos = theme_dict.get(theme_id)
                if pos is not None:
                    tvec[pos] = count

            cos_simi = cos_sim(tvec, user_vec)

            # 遍历simi_users存储目前最大k个值
            index = -1
            gap = 0

            for j in range(len(simi_users)):
                if cos_simi - simi_users[j][1] > gap:
                    gap = cos_simi - simi_users[j][1]
                    index = j

            if index!=-1:
                simi_users[index][0] = tuser_id
                simi_users[index][1] = cos_simi

    table_items = []
    for simi_user in simi_users:
        table_items.append(SimUserTtem(simi_user[0]))

    return table_items