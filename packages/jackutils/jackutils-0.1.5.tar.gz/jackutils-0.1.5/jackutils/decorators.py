#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-06-08


'''
Summary: Class decorator
'''
import functools
import time


def clock(func):
    '''
    计时器，用于计算函数的运行时间
    bug: 接收 lambda 作为参数发生错误
    '''
    @functools.wraps(func)
    def wraps(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)  # 被装饰的func 传入所有参数
        time_delt = time.perf_counter() - t1
        # print(f'{func.__name__}耗时{time_delt}秒')
        print(
            {'func': func.__name__, 'time': time_delt}
        )
        return result
    return wraps


class classproperty(object):
    '''用于将classmethod 装饰为 property'''

    def __init__(self, func):
        self.func = classmethod(func)

    def __get__(self, obj=None, type=None):
        return self.func.__get__(obj, type)()
