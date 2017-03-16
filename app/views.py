# -*- coding:utf-8 -*-
#coding=utf-8

__author__ = 'chenhao'

from app import app
from flask import render_template
from flask import flash
from flask import redirect
from flask import session
from flask import url_for
from flask import request
from forms import InceptionTableStructure
from inception import Inception
from inception_thread import InceptionThread

import MySQLdb
import time

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

        # 通过线程来执行sql，并且只等待线程5秒钟后返回
        inc_thr = InceptionThread(name = db_config_name,
                                  sql = mysql_structure,
                                  is_execute = is_execute)
        inc_thr.setDaemon(True) # 设置成守护进程方式运行
        inc_thr.start()

        start_time = time.time() # 记录thread开始时间

        join_timeout = 5 # 设置 join timeout值
        inc_thr.join(timeout = join_timeout)

        sql_review = inc_thr.get_results()

        end_time = time.time() # 设置结束时间
        join_time = end_time - start_time # 计算线程join等待的时间

        if join_time >= join_timeout:
            print 'join timeout {join_time}s'.format(join_time = join_time)
            return redirect(url_for('.inception_task_list'))
 

        return render_template('dba_tool/inception/inception_execute.html',
                               sql_review = sql_review,
                               abc = mysql_structure,
                               db_config_name = db_config_name,
                               html_select = html_select)

    return render_template('dba_tool/inception/inception_execute.html',
                           html_select = html_select)

# Inception 任务列表
@app.route('/inception/inception_task_list',methods=['GET','POST'])
def inception_task_list():
    """Inceptioni 任务列表"""

    inception = Inception()
    processlist = inception.get_osc_processlist()

    return render_template('dba_tool/inception/inception_task_list.html',
                           processlist = processlist)

# Inception 任务详细信息
@app.route('/inception/inception_task',methods=['GET','POST'])
def inception_task():
    """Inceptioni 任务列表"""

    inception = Inception()

    if request.method == "GET":
        sqlsha1 = request.args.get('sqlsha1')
        percent = inception.get_osc_percent(sqlsha1 = sqlsha1)

    return render_template('dba_tool/inception/inception_task.html',
                           percent = percent)
