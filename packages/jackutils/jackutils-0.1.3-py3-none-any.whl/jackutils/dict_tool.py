#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-06-08

'''
Summary: Dict
'''
import copy


def deep_update_dict(d: dict, u: dict) -> dict:
    # 用于深度 update  dict
    d = copy.deepcopy(d)
    if not u:
        return d
    for k, v in u.items():
        if isinstance(v, dict):
            r = deep_update_dict(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d
