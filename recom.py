# -*- coding:utf-8 -*-
__author__ = 'frank'
from models import Item

def simple_recom(cursor, user_id):
    cursor.execute("select theme_id from user_theme where user_id = '"+user_id+"' order by count desc")
    themes_list = cursor.fetchall()

    num = 5  # 默认推荐数目
    if len(themes_list) < num:  # 如果查询结果少于5，则为查询出来的结果个数
        num = len(themes_list)

    table_itmes = []
    for i in range(num):
        theme_id = themes_list[i][0]

        cursor.execute("select name from themes where id='"+str(theme_id)+"'")
        theme = cursor.fetchone()[0]

        cursor.execute("select gc_id from themes_goodsClass where theme_id = '"+str(theme_id)+"'")
        gc_list = cursor.fetchall()  # 取出频道主题对应的gc_id
        if len(gc_list) > 0:
            for gc in gc_list:
                gc_id = gc[0]
                cursor.execute("select name from goods_class where id = '"+str(gc_id)+"'")
                gc = cursor.fetchone()[0]
                table_itmes.append(Item(theme, gc))

    return table_itmes