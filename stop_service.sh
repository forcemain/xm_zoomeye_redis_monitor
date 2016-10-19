#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Authors: limanman
# 51CTOBG: http://xmdevops.blog.51cto.com/
# Purpose:
#

prog_name='xmzoomeye-redis'
prog_path="`pwd`/${prog_name}"
prog_pids="`pwd`/logs/${prog_name}.pid"
prog_ppid=`(cat ${prog_pids}|grep -o "[^ ]\+\( \+[^ ]\+\)*") 2>/dev/null`

[[ "X${prog_ppid}" != "X" ]] && kill -9 ${prog_ppid} &>/dev/null
> ${prog_pids}
echo -e "Host: $(hostname) Pid: ${prog_ppid:-"None"} Prog: ${prog_path} Status: stop"
