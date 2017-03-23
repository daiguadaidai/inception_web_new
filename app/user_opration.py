#!/usr/bin/env python
#-*- coding:utf-8 -*-

class UserOpration(object):
    """用户操作"""

    def __init__(self):

        admin_user = User()
        admin_user.id = 'Admin.Admin'
        admin_user.username = 'Admin'
        admin_user.password = 'Admin'

        guest_user = User()
        guest_user.id = 'guest.guest'
        guest_user.username = 'guest'
        guest_user.password = 'guest'

        self.users = {
            admin_user.id: admin_user,
            guest_user.id: guest_user,
        }

    def exists(self, username='', password=''):
        """认证用户是否存在"""

        id = '{username}.{password}'.format(username = username,
                                            password = password)

        return self.exists_by_id(id)

    def exists_by_id(self, id=''):
        """认证用户是否存在"""

        if id in self.users:
            return True

        return False

    def get_user_by_name_pass(self, username='', password=''):
        """通过用户名密码获得用户"""
        
        key = '{username}.{password}'.format(username = username,
                                             password = password)

        return self.users.get(key, User())

    def get_user(self, key=''):
        """通过用户名密码获得用户"""
        
        return self.users.get(key, User())

class User(object):

    def __init__(self):
        self.id = ''
        self.username = ''
        self.password = ''

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
