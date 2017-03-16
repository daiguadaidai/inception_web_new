#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'chenhao'

from threading import Thread
from inception import Inception

class InceptionThread(Thread):
    """需要审核的数据库配置保存在这边的变量中"""

    def __init__(self, name='', sql='', is_execute=False):
        Thread.__init__(self)

        self.name = name
        self.sql = sql
        self.is_execute = is_execute
        self.results = []

    def run(self):
        self.results = self.execute_inception()

    def get_results(self):
        """获得审核记录"""
        return self.results

    def execute_inception(self):
        """执行Inception"""
        
        inception = Inception()
        results = inception.sql_review_by_config_name(
                             name = self.name,
                             sql = self.sql,
                             is_execute = self.is_execute)
        return results
