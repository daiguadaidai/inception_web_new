#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'chenhao'

from execute_shell import execute_shell


class MySQLTool(object):
    """调用MySQL官网的mysql tools
    """

    def mysqldiff(self, com_host='127.0.0.1', com_port=3306, com_username='root',
                  com_password='root', com_database='test', com_table='',
                  fra_host='127.0.0.1', fra_port=3306, fra_username='root',
                  fra_password='root', fra_database='test', fra_table='',
                  diff_type='sql'):
        """比较数据库表结构差异
        Args:
            com_host: 完整元数据 host
            com_port: 完整元数据 port
            com_username: 完整元数据 username
            com_password: 完整元数据 password
            com_database: 完整元数据 对比的数据库名
            com_table: 完整元数据 对比的表名

            fra_host: 非完整元数据 host
            fra_port: 非完整元数据 port
            fra_username: 非完整元数据 username
            fra_password: 非完整元数据 password
            fra_database: 非完整元数据 对比的数据库名
            fra_table: 非完整元数据 对比的表名

            diff_type: 对比类型 unified|context|differ|sql
                       unified: 统一标准的
                       context: 内容
                       differ: 差异性
                       sql: 显示SQL语句
        Return:
            比较结果
        """
        com_object = '{db}.{table}'.format(db=com_database, table=com_table) if com_table else com_database
        fra_object = '{db}.{table}'.format(db=fra_database, table=fra_table) if fra_table else fra_database

        cmd = '''
            mysqldiff \
                --server1={com_username}:{com_password}@{com_host}:{com_port} \
                --server2={fra_username}:{fra_password}@{fra_host}:{fra_port} \
                --difftype={diff_type} \
                --changes-for=server2 \
                --force \
                {com_object}:{fra_object}
        '''.format(
            com_host = com_host,
            com_port = com_port,
            com_username = com_username,
            com_password = com_password,
            com_object = com_object,

            fra_host = fra_host,
            fra_port = fra_port,
            fra_username = fra_username,
            fra_password = fra_password,
            fra_object = fra_object,

            diff_type = diff_type,
        )

        is_ok, stdout, stderr = execute_shell(cmd)

        return is_ok, stdout, stderr

def main():
    mysqltool = MySQLTool()

    conf = {
        'com_host': '192.168.2.233',
        'com_port': 3306,
        'com_username': 'HH',
        'com_password': 'oracle12',
        'com_database': 'test',
        'com_table': 'ord_order',

        'fra_host': '192.168.2.233',
        'fra_port': 3306,
        'fra_username': 'HH',
        'fra_password': 'oracle12',
        'fra_database': 'blog',
        'fra_table': 'ord_order',

        'diff_type': 'sql',
    }

    mysqltool.mysqldiff(**conf)


if __name__ == '__main__':
    main()
