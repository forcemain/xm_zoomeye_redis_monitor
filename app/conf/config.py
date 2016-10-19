#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# 51CTOBG: http://xmdevops.blog.51cto.com/
# Purpose:
#
"""
from __future__ import absolute_import


# 说明: 配置基类
class __Config(object):
    # -- flask-mail
    MAIL_PORT = 25
    MAIL_PASSWORD = ''
    MAIL_SERVER = ''
    MAIL_USERNAME = ''
    MAIL_DEFAULT_SENDER = ''

    # -- flask-sqlalchemy
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_NATIVE_UNICODE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///conf/rdsdata.db'

    @staticmethod
    def init_app(app):
        pass


# 说明: 开发环境
class __DevelopmentConfig(__Config):
    pass


# 说明: 预测环境
class __TestingConfig(__Config):
    pass


# 说明: 正式环境
class __ProductionConfig(__Config):
    pass


config = {
    'default': __DevelopmentConfig,
    'develop': __DevelopmentConfig,
    'testing': __TestingConfig,
    'product': __ProductionConfig,
}
