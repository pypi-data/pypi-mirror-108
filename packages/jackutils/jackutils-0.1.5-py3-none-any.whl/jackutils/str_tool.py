#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-06-08

'''
Summary: Str
'''
import string
import random


def generate_random_str(size: int = 6, chars=None, only_number=False):
    '''
    Summary: 生成随机字符串
    '''
    if not chars:
        if not only_number:
            chars = string.ascii_letters + string.digits
        else:
            chars = string.digits
    return ''.join(random.choice(chars) for _ in range(size))
