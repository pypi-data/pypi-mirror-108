#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-05-09

'''
活度相关
'''
from dataclasses import dataclass, field
from jackutils.list_tool import find_x
# activities = {5e-05: (1, 1, 0.95, 0.9),
#           0.0001: (0.995, 0.95, 0.9, 0.83),
#           0.0002: (0.98, 0.94, 0.87, 0.77),
#           0.0005: (0.97, 0.9, 0.8, 0.67),
#           0.001: (0.96, 0.86, 0.73, 0.56),
#           0.002: (0.95, 0.81, 0.64, 0.45),
#           0.005: (0.93, 0.72, 0.51, 0.3),
#           0.01: (0.9, 0.63, 0.39, 0.19),
#           0.02: (0.87, 0.57, 0.28, 0.12),
#           0.05: (0.81, 0.44, 0.15, 0.04),
#           0.1: (0.76, 0.33, 0.08, 0.01),
#           0.2: (0.7, 0.24, 0.04, 0.003),
#           0.3: (0.66, 0.20, 0.03, 0.002),
#           0.5: (0.62, 0.16, 0.02, 0.001),
#           0.7: (0.58, 0.12, 0.01, 0.0005)}
# 默认的活度表
ACTIVITY_DB: dict = {5e-05: (1, 1, 1, 1),
                     0.0001: (0.99, 0.9801, 0.970299, 0.96059601),
                     0.0002: (0.98, 0.9603999999999999, 0.9411919999999999, 0.9223681599999999),
                     0.0005: (0.97, 0.9409, 0.912673, 0.8852928099999999),
                     0.001: (0.96, 0.9216, 0.8847359999999999, 0.8493465599999999),
                     0.002: (0.95, 0.9025, 0.8573749999999999, 0.8145062499999999),
                     0.005: (0.93, 0.8649000000000001, 0.8043570000000001, 0.7480520100000002),
                     0.01: (0.9, 0.81, 0.7290000000000001, 0.6561),
                     0.02: (0.87, 0.7569, 0.658503, 0.57289761),
                     0.05: (0.81, 0.6561000000000001, 0.531441, 0.4304672100000001),
                     0.1: (0.76, 0.5776, 0.43897600000000003, 0.33362176),
                     0.2: (0.7, 0.48999999999999994, 0.3429999999999999, 0.24009999999999995),
                     0.3: (0.66, 0.43560000000000004, 0.28749600000000003, 0.18974736000000003),
                     0.5: (0.62, 0.3844, 0.23832799999999998, 0.14776335999999998),
                     0.7: (0.58, 0.3364, 0.19511199999999995, 0.11316495999999997)}
# 离子强度list
ION_STRENGTH_LIST: list = list(ACTIVITY_DB.keys())


@dataclass
class Activity():
    '''
    Summary: 一个tuple
    '''
    val: tuple = None

    def get(self, valence: int) -> float:
        v = abs(valence)
        if not v:  # =0的情况
            return 0
        return self.val[v-1]


def get_activity(ion_strength: float) -> Activity:
    '''
    Summary: 根据
    '''
    x = find_x(x=ion_strength, y_list=ION_STRENGTH_LIST,
               func=lambda x: x**2)
    val = ACTIVITY_DB.get(x)
    return Activity(val=val)


# @lru_cache(maxsize=128)
# def ion_strength_fx_ions(ions: dict) -> float:
#     '''
#     Summary: 根据ions dt 计算 ion_strength
#     Note   :
#     Return : numbers
#     '''
#     if not ions:
#         return 0
#     # ions = wash_ionsdt(ions)
#     ion_strength = 0
#     for k, v in ions.items():
#         ion = ION_DB.get(k, None)
#         if not ion:
#             continue
#         valence = ion['valence']
#         mmol_l = v
#         ion_strength += get_ion_strength(
#             mmol_l=mmol_l, valence=valence)
#     return ion_strength

# @lru_cache(maxsize=128)
# def yas_fx_ions(ions: dict) -> float:
#     '''
#     Summary: 根据ions dt 计算 yas
#     Note   :
#     Return : numbers
#     '''
#     ion_strength = Activity.ion_strength_fx_ions(ions=ions)
#     return Activity.get_yas(ion_strength=ion_strength)


# @lru_cache(maxsize=128)
# def ksp25ya_fx_molecule_ions_strength(molecule_name, ion_strength=0):
#     '''
#     Summary: 根据化合物名称、溶液 ion strength 计算此时的ksp25ya
#     Note   :
#     Return : number
#     para1  : molecule_name 化合物名称
#     para2  : ion strength
#     '''
#     ml = MOLECULE_DB.get(molecule_name)
#     yas = Activity.get_yas(ion_strength)
#     xa, xb, va, vb, ksp25 = ml['xa'], ml['xb'], ml['va'], ml['vb'], ml['ksp25']
#     ya = yas.get_ya(valence=va)
#     yb = yas.get_ya(valence=vb)
#     return ksp25 / (ya**xa * yb**xb)
