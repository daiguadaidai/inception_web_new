# -*- coding:utf-8 -*-
#coding=utf-8
__author__ = 'chenhao'

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_script import Manager
from flask_login import LoginManager


app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True
app.config.from_object('config')
toolbar = DebugToolbarExtension(app)

manager = Manager(app)

# login
lm = LoginManager()
lm.session_protection = 'strong'
lm.login_view = 'login'
lm.init_app(app)

from app import views, forms
