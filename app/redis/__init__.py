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
from flask import Blueprint
# 说明: 导入其它模块


redis = Blueprint('redis', __name__, static_folder='static', template_folder='templates')

from . import api
from . import views
from . import error
