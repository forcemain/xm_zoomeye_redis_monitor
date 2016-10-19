#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# OsChina: http://xmdevops.blog.51cto.com/
# Purpose:
#
"""
# 说明: 导入公共模块
import time
from .wrappers import singleton
from redis import StrictRedis, RedisError
# 说明: 导入其它模块


@singleton
class Redis(object):
    def __init__(self, timeout=1):
        self.servers = {}
        self.timeout = timeout

    def ping(self, host, port, password):
        result = {'success': 0}
        if all([host, port]):
            try:
                rds = StrictRedis(host, port, password)
                rds.ping()
                result.update({'success': 1})
            except RedisError, e:
                pass
            return result
        return result

    def info(self, host, port, password, identify):
        result = {'success': 0, 'data': ''}
        if not all([host, port]):
            return result
        if identify in self.servers:
            cur_time = time.time()
            if cur_time - self.servers[identify]['time'] > self.timeout:
                result = self.reqs(identify, host, port, password)
            else:
                result.update({
                    'success': 1,
                    'data': self.servers[identify]['info'],
                })
        else:
            result = self.reqs(identify, host, port, password)
        return result

    def reqs(self, identify, host, port, password):
        info = {}
        result = {'success': 0, 'data': ''}

        try:
            start_time = time.time()
            rds = StrictRedis(host, port, password)
            info = rds.info()
            end_time = time.time()
            info.update({'get_time': end_time-start_time})
            result.update({
                'success': 1,
                'data': info
            })
        except RedisError, e:
            pass
        self.servers[identify] = {}
        self.servers[identify].update({
            'time': time.time(),
            'info': info
        })
        return result
