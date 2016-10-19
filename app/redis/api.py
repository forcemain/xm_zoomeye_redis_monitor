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
import pprint
from redis import RedisError
from flask import jsonify, render_template, request
# 说明: 导入其它模块
from .. import db
from . import redis
from ..libs.database import Redis
from ..models import RdsInstances


@redis.route('/api/redis/ping', methods=['POST'])
def redis_ping():
    result = {'success': 0}
    rds_host = request.form.get('rds_host')
    rds_pass = request.form.get('rds_pass')
    rds_port = request.form.get('rds_port')
    try:
        Redis().ping(rds_host, rds_port, rds_pass)
        result.update({'success': 1})
    except RedisError, e:
        pass
    return jsonify(result)


@redis.route('/api/redis/add', methods=['POST'])
def redis_add():
    result = {'success': 0}
    rds_host = request.form.get('rds_host')
    rds_pass = request.form.get('rds_pass')
    rds_port = request.form.get('rds_port')
    usermail = request.form.get('usermail')
    add_time = request.form.get('add_time')
    rds = RdsInstances.query.filter_by(rds_host=rds_host, rds_port=rds_port).all()
    if rds:
        return jsonify(result)

    rds = RdsInstances(
        rds_host=rds_host, rds_pass=rds_pass,
        rds_port=rds_port, usermail=usermail,
        add_time=add_time, enctoken=add_time)

    db.session.add(rds)
    db.session.commit()

    result.update({'success': 1})
    return jsonify(result)


@redis.route('/api/redis/delete', methods=['POST'])
def redis_delete():
    result = {'success': 0}
    identify = request.form.get('identify')
    rds = RdsInstances.query.filter_by(identify=identify).first()
    if not rds:
        return jsonify(result)
    db.session.delete(rds)
    db.session.commit()
    result.update({'success': 1})
    return jsonify(result)


@redis.route('/api/redis/json', methods=['POST'])
def redis_json():
    result = {'success': 0, 'data': ''}
    identify = request.form.get('identify')
    rds = RdsInstances.query.filter_by(identify=identify).first()
    if not rds:
        return jsonify(result)
    rds_host = rds.rds_host
    rds_pass = rds.rds_pass
    identify = rds.identify
    rds_port = int(rds.rds_port)
    result = Redis().info(rds_host, rds_port, rds_pass, identify)
    return jsonify(result)
