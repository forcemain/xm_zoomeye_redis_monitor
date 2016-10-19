#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://xmdevops.blog.51cto.com/
# Purpose:
#
"""
from __future__ import absolute_import
# 说明: 导入公共模块
from flask import render_template
# 说明: 导入其它模块
from . import redis


@redis.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html')


@redis.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html')
