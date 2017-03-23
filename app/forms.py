# -*- coding:utf-8 -*-
#coding=utf-8
__author__ = 'chenhao'

from flask_wtf import Form
from wtforms import TextAreaField
from wtforms import SubmitField
from wtforms import validators
from wtforms import StringField
from wtforms.validators import Required

class InceptionTableStructure(Form):
    table_name = TextAreaField('请输入需要评审的表结构: ', validators=[Required()])
    submit = SubmitField('Submit')

class LoginForm(Form):
    username = StringField('请输入用户名', default='', validators=[Required()])
    password = StringField('请输入密码', default='', validators=[Required()])
    submit = SubmitField('登录')
