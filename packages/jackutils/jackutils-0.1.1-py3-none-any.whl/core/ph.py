#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-05-09

'''
Summary: PH相关
'''

from dataclasses import dataclass
from typing import Optional
import math
import copy
# app
from .temp import Temp
from .water_utils import h_mol_fx_A, h_mol_fx_ph


@dataclass
class PhDc:
    '''
    PH class, 包含一系列ph相关计算的类
    OH 和 H 看似 可以通过H*OH = KW 限制
    其实不然
    需要以 H-OH 的差值作为唯一依据
        - 质子平衡时 不考虑 活度
        - K1 K2 平衡需要考虑活度
        - H*OH = kw (其实等于  H_active * OH_active = kw)
        - H和OH都是abs(valence) = 1 
        - 因此 kw / activity_k**2 = H*OH
        - 单位都是 mol/l
    '''
    temp: float = 25  # 温度
    y1: float = 1  # 1价活度
    T: Temp = None
    h: float = 0  # 最终 h 实际质子平衡
    oh: float = 0  # 最终oh_mol 实际质子平衡
    # 计算
    y1: float = None  # 1价离子 活度
    a0a1a2: dict = None  # 碳酸平衡比例
    A: Optional[float] = None  # A
    ph: Optional[float] = None  # ph

    def __post_init__(self):
        if not self.T:
            self.T = Temp(self.temp)
        self.set_by_ph()
        self.set_by_A()
        self.set_a0a1a2()

    def set_by_ph(self):
        # 通过ph设定
        if self.ph is None:
            return None
        self.h = h_mol_fx_ph(ph=self.ph, y1=self.y1)
        self.oh_active = self.T.kw / self.h_active
        self.A = self.h-self.oh

    def set_by_A(self):
        if self.A is None:
            return None
        self.h = h_mol_fx_A(A=self.A, kw=self.T.kw, y1=self.y1)
        self.oh_active = self.T.kw / self.h_active
        self.ph = -math.log10(self.h_active)

    @property
    def h_active(self) -> float:
        '''考虑活度的[h]'''
        return self.h * self.y1

    @h_active.setter
    def h_active(self, val: float):
        '''考虑活度的[h]'''
        self.h = val / self.y1

    @property
    def oh_active(self) -> float:
        '''考虑活度的[oh]'''
        return self.oh * self.y1

    @oh_active.setter
    def oh_active(self, val: float):
        '''考虑活度的[h]'''
        # val = validate_numbers(val)
        self.oh = val / self.y1

    def set_a0a1a2(self):
        '''
        Summary: 设置co2 hco3 co3 比例,初始化时候运行
        Depend : self.ph
        Note   : 如果传入实际的ct，应该考虑 co2溢出的可能，因此比例增加一个co2gas(ag)
        Return : dict
        '''
        h = self.h_active
        k1 = self.T.k1
        k2 = self.T.k2
        ka_nh4 = self.T.ka_nh4
        if self.h >= 1:
            nh3 = 0
        elif self.oh >= 1:
            nh3 = 1
        else:
            nh3 = ka_nh4/(h + ka_nh4)
        nh4 = 1 - nh3
        # 不考虑活度
        # a0 = (h**2) / (h**2 + k1 * h + k1 * k2)
        a1 = (k1*h) / (h**2 + k1 * h + k1 * k2)
        a2 = k1*k2 / (h**2 + k1 * h + k1 * k2)
        a0 = 1-a1-a2
        ag = 0
        self.a0a1a2 = dict(a0=a0, a1=a1, a2=a2, ag=ag, nh3=nh3, nh4=nh4)

    def a0a1a2_with_ct(self, ct: float) -> dict:
        '''
        Summary: 根据当前的a0a1a2比例 传入ct，不考虑co2气体溢出可能
        Depend : self.a0a1a2
        Return : dict，实际的 co2g co2 hco3 co3
        para1  : ct： 总C mmol_l
            - return的单位与 传入ct一致
        '''
        aaa = copy.copy(self.a0a1a2)  # 复制一份
        aaa['ag'] = 0  # co2气体部分
        a0, a1, a2 = aaa['a0'], aaa['a1'], aaa['a2']
        dt = {}
        # if a0*ct > 10:
        #     new_ct = 10/a0  # new ct
        # else:
        #     new_ct = ct
        new_ct = ct
        dt['co2'] = new_ct*a0
        dt['hco3'] = new_ct*a1
        dt['co3'] = new_ct*a2
        # 增加 'ag'部分，在 H 平衡时，也要考虑此部分包含的质子
        dt['ag'] = ct-new_ct  # 此部分转换为 ag了
        dt['h_in_ct'] = (dt['co2']+dt['ag'])*2 + dt['hco3']
        return dt

    @property
    def h_in_h2co3_k(self):
        '''碳酸体系 包含 H'''
        return self.a0a1a2['a0'] * 2 + self.a0a1a2['a1']

    @property
    def h_in_nh3_k(self) -> float:
        '''氨体系 包含的 H: 仅 nh4 包含 H '''
        return self.a0a1a2['nh4']
