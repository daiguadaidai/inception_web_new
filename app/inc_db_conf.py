#!/usr/bin/env python
#-*- coding:utf-8 -*-

class IncDbConf(object):
    """inception数据库而配置信息
    这边配置信息比较简单, 我们直接使用python的dict来代替
    """

    def __init__(self):

        self.inc_configs = {
            'one': {
                'host': '127.0.0.1',
                'port': 3306,
                'port': 6669,
                'use_unicode': True,
                'charset': 'utf8mb4',
            },

            'two': {
                'host': 'xxx.xxx.xxx.xxx',
                'port': 3306,
                'port': 6669,
                'use_unicode': True,
                'charset': 'utf8mb4',
            },
        }

        self.db_configs = {
            'xxx': {
                'host': '127.0.0.1',
                'port': 3306,
                'username': 'etl',
                'password': 'etl',
                'database': 'xxx',
                'name': 'xxx', # 和key的名称是一样的
                'alias': 'xxx',
            },

            'yyy': {
                'host': '127.0.0.1',
                'port': 3306,
                'username': 'etl',
                'password': 'etl',
                'database': 'yyy', # 和key的名称是一样的
                'name': 'yyy',
                'alias': 'yyy',
            },
        }


def main():
    pass


if __name__ == '__main__':
    main()
