#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhangjunbo@meituan.com
@time: 2017/6/18 上午12:12
@desc:
"""


# 转化json对象
def convert_to_json(obj):
    d = {}
    d.update(obj.__dict__)
    return d
