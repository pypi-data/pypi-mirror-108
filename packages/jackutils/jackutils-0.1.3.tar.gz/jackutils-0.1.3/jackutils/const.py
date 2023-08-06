#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# File    :   const.py
# Time    :   2019/01/14 00:09:45
# Author  :   Jack Li
# Contact :   allanth3@163.com

'''常量 & 数据库连接'''
import math

PI = math.pi
GB9119 = {
    # 10:'3/8 inch',
    15: '1/2 inch',
    20: '3/4 inch',
    25: '1 inch',
    32: '1 1/4 inch',
    40: '1 1/2 inch',
    50: '2 inch',
    65: '2 1/2 inch',
    80: '3 inch',
    100: '4 inch',
    125: '5 inch',
    150: '6 inch',
    200: '8 inch',
    250: '10 inch',
    300: '12 inch',
    350: '14 inch',
    400: '16 inch',
    500: '20 inch',
}
DN_LIST = list(GB9119.keys())
# 电机标准功率
KW_LIST = [
    0.15,
    0.22,
    0.37,
    0.55,
    0.75,
    1.1,
    1.5,
    2.2,
    3,
    4,
    5.5,
    7.5,
    11,
    15,
    18.5,
    22,
    30,
    37,
    45,
    55,
    75,
    90,
    110,
    132,
    160,
    185,
    200
]
# BLADE_D_LIST = [x*500 for x in range(1, 13)]  # 搅拌机 桨叶尺寸
BLADE_D_LIST = [  # 搅拌机 桨叶尺寸
    350,
    400,
    450,
    500,
    550,
    600,
    700,
    800,
    900,
    1000,
    1100,
    1200
]
TANK_V_GENERAL_LIST = [
    x/10 for x in range(1, 50)] + [x for x in range(5, 501)]
PN_LIST = [  # 压力表 压力等级 bar
    6,
    10,
    20,
    25,
    40,
    50,
    60,
    100,
    160,
]
HEAT_EXCHANGE_KW = {
    0.5: 0.37,
    1: 0.55,
    1.5: 0.75,
    2: 1.1,
    3: 1.5,
    4: 2.2,
    5: 3,
    6: 4,
    8: 5.5,
    10: 7.6,
    15: 11,
    20: 15
}
