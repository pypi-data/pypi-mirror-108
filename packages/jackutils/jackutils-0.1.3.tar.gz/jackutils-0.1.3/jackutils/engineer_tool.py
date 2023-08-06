#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-06-08

'''
Summary: 工程参数
'''
import numbers
from . import const
from .list_tool import find_x


def get_standard_dn(val: numbers.Real, max_val=None, min_val=None):
    '''
    Summary: 获得GB标准中的DN（平方取最近）
    '''
    ls = const.DN_LIST
    if val in ls:
        return val
    return find_x(x=val, y_list=ls, func=lambda x: x**2, maximum=max_val, minium=min_val)


def get_standard_pn(val: numbers.Real, max_val=None, min_val=None):
    '''
    Summary: 获得标准PN（取大）
    '''
    ls = const.PN_LIST
    if val in ls:
        return val
    return find_x(x=val, y_list=ls, use_larger=True, maximum=max_val, minium=min_val)


def get_standard_kw(val: numbers.Real, max_val=None, min_val=None):
    '''
    Summary: 获得标准kw(最近)
    '''
    ls = const.KW_LIST
    if val in ls:
        return val
    return find_x(x=val, y_list=ls, maximum=max_val, minium=min_val)
