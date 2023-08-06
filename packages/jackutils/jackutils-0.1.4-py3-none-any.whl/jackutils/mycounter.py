#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# File    :   names.py
# Time    :   2019/01/25 00:06:46
# Author  :   Jack Li
# Contact :   allanth3@163.com

'''
Ions Names Dict
完全继承Dict

手动加上 加减乘除 4个方法
'''

import copy
import numbers
from collections import Counter


class MyCounter(Counter):
    '''
    Summary: 以namedtuple 作为key 的dict
    Note   : 实现dict的基本数学运算
    '''

    @property
    def all_names(self):
        '''
        Summary: 所有namedtuple的name属性list
        Note   : 有普通的key则返回空列表
        Return : list
        '''
        try:
            return [x.name for x in self.keys()]
        except:
            return []

    @classmethod
    def from_dict(cls, dt):
        '''
        从普通dt生成MyCounter()
        key小写化，去除v 非数字或0
        **True 是 numbers.Real
        '''
        new = {str(k).lower(): v for k,
               v in dt.items() if v and isinstance(v, numbers.Real) and not isinstance(v, bool)}
        return cls(new)

    def __imul__(self, i: float):
        '''self *= i'''
        self = MyCounter({k: v*i for k, v in self.items()})

    def __mul__(self, i: float):
        '''self * i'''
        new = {k: v*i for k, v in self.items()}
        return MyCounter(new)

    def __rmul__(self, i: float):
        '''i * self'''
        return self.__mul__(i)

    def __truediv__(self, i: float):
        '''self / i'''
        new = {k: v/i for k, v in self.items()}
        return MyCounter(new)

    def __itruediv__(self, i: float):
        '''self /= i '''
        self = MyCounter({k: v/i for k, v in self.items()})

    def __add__(self, other):
        '''like Counter __add__ but return MyCounter'''
        #cls = type(self)
        if other is None:
            return copy.copy(self)
        return MyCounter(super().__add__(other))

    def __iadd__(self, other):
        '''like Counter __iadd__ but return MyCounter'''
        #cls = type(self)
        if other is None:
            return copy.copy(self)
        return super().__iadd__(other)

    def __sub__(self, other):
        '''like Counter __sub__ but return MyCounter'''
        #cls = type(self)
        if other is None:
            return copy.copy(self)
        return MyCounter(super().__sub__(other))

    def __isub__(self, other):
        '''like Counter __isub__ but return MyCounter'''
        #cls = type(self)
        if other is None:
            return copy.copy(self)
        return super().__isub__(other)
