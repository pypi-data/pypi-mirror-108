#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-06-08

from typing import List
import math


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
