# -*- coding:utf-8 -*-
from flask import Flask, render_template, request
from flask_bootstrap3 import Bootstrap
from flaskext.mysql import MySQL
import recom
from models import GoodsTable, SimUserTable

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '34092402'
app.config['MYSQL_DATABASE_DB'] = 'ad_recom'
app.config['MYSQL_DATABASE_CHARSET'] = 'gb2312'
mysql = MySQL(app)


# 路由函数
@app.route('/')
def index():
    user_id = request.args.get("user_id")  # 获取get参数中的user_id
    if user_id != '' and user_id is not None:  # 判空
        cursor = mysql.connect().cursor()

        user_name = recom.find_user_name(cursor, user_id)
        items = recom.simple_recom(cursor, user_id)
        if len(items) > 0:
            goods_table = GoodsTable(items, classes=['goodsTable', 'table'])

            usersItem = recom.find_similar_users(cursor, user_id)
            sim_user_table = SimUserTable(usersItem, classes=['simiUserTable', 'table'])
            return render_template("index.html", goods_table=goods_table, simi_users_table=sim_user_table,
                                   userId=user_id, userName=user_name)
        else:
            return render_template("index.html", userId=user_id, userName=user_name)
    else:
        return render_template("index.html")

@app.route('/test/<user_id>')
def test(user_id=None):
    cursor = mysql.connect().cursor()
    return str(recom.find_similar_users(cursor, user_id))

if __name__ == '__main__':
    app.run(debug=True)
    bootstrap = Bootstrap(app)