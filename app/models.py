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
import hashlib
# 说明: 导入其它模块
from . import db


class RdsInstances(db.Model):
    __tablename__ = 'RdsInstances'
    id = db.Column(db.Integer(), primary_key=True)
    rds_host = db.Column(db.String(32), unique=False, nullable=False, index=True)
    rds_port = db.Column(db.String(32), unique=False, nullable=False, index=True)
    add_time = db.Column(db.String(32), unique=False, nullable=False, index=True)
    rds_pass = db.Column(db.String(32), unique=False, nullable=True, index=True)
    usermail = db.Column(db.String(32), unique=False, nullable=True, index=True)
    identify = db.Column(db.String(64), unique=True, nullable=False, index=True)

    @property
    def enctoken(self):
        pass

    @enctoken.setter
    def enctoken(self, s):
        m = hashlib.md5()
        m.update(s)
        self.identify = m.hexdigest()
