#!/usr/bin/env python
#-*- coding:utf-8 -*-

from inc_db_conf import IncDbConf

import MySQLdb


class Inception(object):
    """需要审核的数据库配置保存在这边的变量中"""

    def __init__(self):
        inc_db_conf = IncDbConf()

        # 获取 Inception 软件配置信息
        self.inc_configs = inc_db_conf.inc_configs

        # 获取目标审核库信息数据库而配置信息
        self.db_configs = inc_db_conf.db_configs

    def _row_to_dicts(self, col_names=[], rows=[]):
        """将给定的字段名和结果集拼凑成一个dict结果集
        Args
            col_names: 字段名 ['age', 'name']
        Return
            返回一个dict数组
            [{'age': 11, 'name': 'HH'},
             {'age': 12, 'name': 'ZS'}]
        Raise: None 
        """

        return [
            self._row_to_dict(col_names, row)
            for row in rows
        ]


    def _row_to_dict(self, col_names=[], row=[]):
        """将给定的字段名和结果集拼凑成一个dict结果集
        Args
            col_names: 字段名 ['age', 'name']
        Return
            返回一个dict
            {'age': 11, 'name': 'HH'}
        Raise: None
        """

        return dict(zip(col_names, row))



    def get_db_config(self, db_key=''):
        """获取通过传入的一个key获取数据库连接信息

        Args:
            db_key: 这个参数值应该和self.db_configs dict 中的key匹配

        Return: 一个数据库的链接信息
                db_config = {
                    'host': '127.0.0.1',
                    'port': 3306,
                    'username': 'xxx',
                    'password': 'xxx',
                    'database': '',
                    'name': 'xxx',
                    'alias': '133测试线-xx',
                }

        Raise: None
        """

        return self.db_configs.get(db_key, None)

    def get_db_info_to_html_select(self):
        """获取数据库配置的名称和别名

        Args: None

        Return: 返回所有数据库的名称和别名
                html_select = {
                    'yyy': {
                        'name': 'yyy',
                        'alias': '133测试线-yyy',
                    },

                    'xxx': {
                        'name': 'xxx',
                        'alias': '133测试线-xxx',
                    },
                }

        Raise: None
        """

        html_select = {}

        for key, db_config in self.db_configs.iteritems():
            name_and_alias = {}
            name_and_alias['name'] = db_config['name']
            name_and_alias['alias'] = db_config['alias']

            html_select[key] = name_and_alias
      

        return html_select

    def sql_review_by_detail(self, host='127.0.0.1', port=3306,
            is_execute=False, username='root', password='root', sql=''):
    
        action = '--execute=1' if is_execute else '--check=1'
    
        # 拼凑 inception 需要的 SQL
        sql = '''
        /*--user={username};--password={password};--host={host};{action};--port={port};*/
    
        inception_magic_start;
    
        use nbuy52db;
    
        {sql}
    
        inception_magic_commit;
        '''.format(username = username,
                   password = password,
                   host = host,
                   port = port,
                   action = action,
                   sql = sql)
    
    
        try:
            conn = MySQLdb.connect(**self.inc_configs['two'])
            cur = conn.cursor()
            ret = cur.execute(sql)
            result = cur.fetchall()
    
            field_names = [i[0] for i in cur.description]
    
            sql_review = self._row_to_dicts(field_names, result)
    
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    
        return sql_review

    def sql_review_by_config_name(self, name='', sql='', is_execute=False):
        """通过获取的需要审核的数据库配置名和相关SQL进行审核

        Args: 
            name: 配置名称
            sql: sql语句
            is_execute: 是否执行

        Return: 审核的SQL结果
        Raise: None
        """

        db_config = self.db_configs.get(name, None)

        print db_config

        if not db_config:
            return []

        sql_review = self.sql_review_by_detail(
                                     host = db_config.get('host', '127.0.0.1'),
                                     port = db_config.get('port', 3306),
                                     is_execute = is_execute,
                                     username = db_config.get('username', 'root'),
                                     password = db_config.get('password', 'root'),
                                     sql = sql)

        return sql_review

    def execute_inc_sql(self, sql=''):
        """执行inception SQL获取inception相关信息
        Args
            sql: 需要执行的sql
        Return
            返回执行的结果
        Raise: None
        """
        conn = MySQLdb.connect(self.inc_configs['two'])
        cur = conn.cursor()
        ret = cur.execute(sql)
        result = cur.fetchall()

        return result

def main():
    inception = Inception()

    print inception.get_db_config('nbuy52db_3306117133')

    print inception.get_db_info_to_html_select()


if __name__ == '__main__':
    main()
