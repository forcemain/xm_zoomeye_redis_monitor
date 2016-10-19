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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# 说明: 导入其它模块
from .conf.config import config


db = SQLAlchemy()
app = Flask(__name__)


def create_app(env='default'):
    app.config.from_object(config[env])

    db.init_app(app)

    from .redis import redis as redis_blueprint
    app.register_blueprint(redis_blueprint)
    return app
