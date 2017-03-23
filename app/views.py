# -*- coding:utf-8 -*-
#coding=utf-8

__author__ = 'chenhao'

from app import app
from app import lm
from flask import render_template
from flask import flash
from flask import redirect
from flask import session
from flask import url_for
from flask import request
from flask import g
from flask_login import login_user
from flask_login import login_required
from flask_login import current_user
from flask_login import logout_user
from forms import InceptionTableStructure
from forms import LoginForm
from inception import Inception
from inception_thread import InceptionThread
from user_opration import UserOpration
from user_opration import User

import MySQLdb
import time

@app.route('/')
@app.route('/index')
@login_required
def index():
    """首页"""

    return render_template("index.html")


@lm.user_loader
def load_user(user_id):
    user_opration = UserOpration()
    user = user_opration.get_user(key = user_id)
    session['username'] = user.username
    return user


@app.before_request
def before_request():
    g.user = current_user 


@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录界面"""

    form = LoginForm()

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user_opration = UserOpration()
        user = user_opration.get_user_by_name_pass(username=username,
                                                   password=password)

        if form.validate_on_submit(): # 验证通过, 登录用户
            login_user(user)

            return redirect(url_for('.index'))
        else: # 验证失败
            if not user_opration.exists(username=username, password=password): # 如果已经登录过则退出
                logout_user()

            flash('用户名密码验证失败!')

            return render_template("login.html", form = form)

    if request.method == 'GET':

        if g.user.__dict__: # 如果没有退出用户, 转跳到 index 页面
            return redirect(url_for('.index'))
        
        return render_template("login.html", form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/inception/inception_check',methods=['GET','POST'])
def inception_check():
    """Inception_评审SQL"""

    if not g.user.__dict__: # 如果没有登录就不显示 username
        session['username'] = ''

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


@app.route('/inception/inception_execute',methods=['GET','POST'])
@login_required
def inception_execute():
    """Inception_执行SQL"""

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


@app.route('/inception/inception_task_list',methods=['GET','POST'])
@login_required
def inception_task_list():
    """Inception 任务列表"""

    inception = Inception()
    processlist = inception.get_osc_processlist()

    return render_template('dba_tool/inception/inception_task_list.html',
                           processlist = processlist)


@app.route('/inception/inception_task',methods=['GET','POST'])
@login_required
def inception_task():
    """Inception 任务详细信息"""

    inception = Inception()

    if request.method == "GET":
        sqlsha1 = request.args.get('sqlsha1')
        percent = inception.get_osc_percent(sqlsha1 = sqlsha1)

    return render_template('dba_tool/inception/inception_task.html',
                           percent = percent)


@app.route('/inception/inception_task_stop',methods=['GET', 'POST'])
@login_required
def inception_task_stop():
    """停止Inception任务"""

    inception = Inception()

    if request.method == "POST":
        sqlsha1 = request.form.get('sqlsha1')
        is_ok, result = inception.inc_stop_alter(sqlsha1 = sqlsha1)

        import simplejson as json
        return json.dumps({'is_ok': is_ok, 'result': result})
