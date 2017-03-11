# -*- coding:utf-8 -*-
#coding=utf-8
__author__ = 'lihui'

from app import app
from flask import render_template
from flask import flash
from flask import redirect
from flask import session
from flask import url_for
from flask import request
from forms import InceptionTableStructure
from inception import Inception

import MySQLdb

#首页
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

#Inception_评审SQL
@app.route('/inception/inception_check',methods=['GET','POST'])
def inception_check():

    form = InceptionTableStructure()

    # inception 实例
    inception = Inception()
    html_select = inception.get_db_info_to_html_select()

    sql_review = []

    if request.method == "POST":
        # 获取需要在 Inception 中执行的参数
        mysql_structure = request.form.get('mysql_structure')
        db_config_name = request.form.get('db_config_name')
        is_execute = False

        # 通过选择的数据库名进行 sql review
        sql_review = inception.sql_review_by_config_name(
                                     name = db_config_name,
                                     sql = mysql_structure,
                                     is_execute = is_execute)

        return render_template('dba_tool/inception/inception_check.html',
                               sql_review = sql_review,
                               abc = mysql_structure,
                               db_config_name = db_config_name,
                               html_select = html_select)

    return render_template('dba_tool/inception/inception_check.html',
                           html_select = html_select)


#Inception_执行SQL
@app.route('/inception/inception_execute',methods=['GET','POST'])
def inception_execute():

    form = InceptionTableStructure()

    # inception 实例
    inception = Inception()
    html_select = inception.get_db_info_to_html_select()

    sql_review = []

    if request.method == "POST":
        # 获取需要在 Inception 中执行的参数
        mysql_structure = request.form.get('mysql_structure')
        db_config_name = request.form.get('db_config_name')
        is_execute = True

        # 通过选择的数据库名进行 sql review
        sql_review = inception.sql_review_by_config_name(
                                     name = db_config_name,
                                     sql = mysql_structure,
                                     is_execute = is_execute)

        return render_template('dba_tool/inception/inception_execute.html',
                               sql_review = sql_review,
                               abc = mysql_structure,
                               db_config_name = db_config_name,
                               html_select = html_select)

    return render_template('dba_tool/inception/inception_execute.html',
                           html_select = html_select)
