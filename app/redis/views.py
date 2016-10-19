#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://xmdevops.blog.51cto.com/
# Purpose:
#
"""
# from __future__ import absolute_import
# 说明: 导入公共模块
from flask import render_template, url_for, redirect
# 说明: 导入其它模块
from . import redis
from ..models import RdsInstances


@redis.route('/', methods=['GET'])
def index():
    redis_list = RdsInstances.query.all()
    return render_template('index.html', redis_list=redis_list)


@redis.route('/redis/<identify>.html', methods=['GET'])
def redis_monitor(identify):
    rds = RdsInstances.query.filter_by(identify=identify).first()
    if not rds:
        return redirect(url_for('redis.index'))
    return render_template('monitor.html', redis=rds)
