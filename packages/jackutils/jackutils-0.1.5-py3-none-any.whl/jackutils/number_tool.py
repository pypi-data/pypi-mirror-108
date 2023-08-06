#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-06-08

'''
Summary:number
'''


def validate_numbers(val: float, ge_zero: bool = True, throw: bool = False, default: float = 0):
    '''
    验证传入值是否数字，并且符合要求
    ge_zero: 必须 >= 0
    throw:抛出错误，如果设置为False  则返回 default
    '''
    try:
        val = float(val)
    except:
        if throw:
            raise TypeError('val 必须是数字')
        else:
            return default
    if ge_zero:
        if val < 0:
            if throw:
                raise ValueError(f'Value{val} < 0')
            else:
                return default
    return val
