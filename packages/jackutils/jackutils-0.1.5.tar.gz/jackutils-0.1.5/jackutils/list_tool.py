#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-06-08

from typing import List, Sequence
import math
import numbers
import bisect
import itertools


def gcd_many(s: List[int]) -> int:
    '''
    Summary: 求一组数字的 最大公约数
    '''
    g = 0
    for i in range(len(s)):
        if i == 0:
            g = s[i]
        else:
            # math.gcd 可以求2个数字的最大公约数
            g = math.gcd(g, s[i])
    return g


def flat_and_sort_list(ls: List) -> list:
    '''列表降维 + 排序'''
    ls = list(itertools.chain(*ls))
    ls.sort()
    return ls


def find_x(x: numbers.Number,
           y_list: List[numbers.Number],
           use_smaller: bool = False,
           use_larger: bool = False,
           func=None,
           maximum: numbers.Number = None,
           minium: numbers.Number = None):
    '''
    从list中找到 参数1 最接近的值，或者小于/大于的值
    Params:
        - x: numbers.Number, 原始值
        - y_list: List[numbers.Number], 列表
        - use_smaller: bool = False, True则找到最接近的比原始值小的值
        - use_larger: bool = False, True 则找到最接近的比原始值大的值
        - func: bool = False, True 则采用 fun(x)的值作为对比
        - maximum: numbers.Number = None, 提供的话则限制最大值不超过此值
        - minium: numbers.Number = None, 提供则限制最小值不小于此值
    '''
    if not isinstance(x, numbers.Number):
        raise TypeError('find_x 只能处理数字')
    if not isinstance(y_list, Sequence) or not y_list:
        raise TypeError('y_list 应为List[float]')
    y_list.sort()  # 进行正向排序
    # 如果限定了最大值(限定在 y_list之间才有意义)
    if maximum and maximum >= y_list[0] and maximum <= y_list[-1]:
        y_list = y_list[:bisect.bisect(y_list, maximum)]  # 切片到<=maximum的值
    # 如果限定了最小值(限定在 y_list之间才有意义)
    if minium and minium >= y_list[0] and minium <= y_list[-1]:
        y_list = y_list[bisect.bisect_left(y_list, minium):]  # 切片到>=maximum的值
    # 寻找合适额值
    if x in y_list:
        return x
    # 如果比最小值还小
    elif x < y_list[0]:
        return y_list[0]
    elif x > y_list[-1]:
        return y_list[-1]
    else:
        index = bisect.bisect(y_list, x)
        small = y_list[index-1]
        large = y_list[index]
        if use_smaller:  # 如果需要找到小的
            return small
        elif use_larger:  # 如果需要找到大的
            return large
        else:  # 根据条件找到最靠近的
            if not func:  # 是否使用平方数代替直接的对比（考虑到管径选择时候选用直径平方更加合适 math.pow）
                return small if (small+large)/2 >= x else large  # 对应的离子强度标定
            else:
                return small if (func(small) + func(large))/2 >= func(x) else large
