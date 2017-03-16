#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding=utf-8


from __future__ import unicode_literals
__author__ = 'chenhao'

from app import app,manager
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    manager.run()
