#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-05-09

'''
温度
'''
from dataclasses import dataclass
from functools import lru_cache
# app
from .fomulas import get_water_dynamic_viscosity, get_temp_correction_factor

'''
[温度相关系数 经验公式]
1) pk1 : [H][HCO3] == [H2CO3]
2) pk2 : [H][CO3] == [HCO3]
3) pkw : [H][OH] == [H2O]
4) pkh : ??
5) pks : ?? (CaCO3)
'''


@lru_cache(maxsize=128)
@dataclass
class Temp:
    temp: float = 25  # 默认为摄氏度 非绝对温度

    @property
    def K(self) -> float:
        return self.temp + 273.15

    @property
    def F(self) -> float:
        '''
        Summary: 华氏温度
        '''
        return self.temp*1.8+32

    @property
    def RA(self) -> float:
        '''
        Summary: 兰氏度Rankine
        '''
        return self.temp * 1.8 + 32 + 459.67

    @property
    def R(self) -> float:
        '''
        Summary: 列氏度Réaumur
        '''
        return self.temp * 0.8

    @property
    def pk1(self) -> float:
        # return 3447/self.K-15.08 + 0.0331*self.K
        return 6.38

    @property
    def pk2(self) -> float:
        # return 2929/self.K - 6.65 + 0.0240 * self.K
        return 10.21

    @property
    def pkw(self) -> float:
        return 4470/self.K - 6.09 + 0.0171*self.K

    @property
    def pkh(self) -> float:
        return -2218/self.K + 12.7 - 0.0127*self.K

    @property
    def pks(self) -> float:
        return 8.03 + 0.01183*self.K

    @property
    def k1(self) -> float:
        return 10**(-self.pk1)

    @property
    def k2(self) -> float:
        return 10**(-self.pk2)

    @property
    def kw(self) -> float:  # 稀溶液中水的kw
        if self.temp == 25:
            return 1e-14
        return 10**(-self.pkw)

    @property
    def kh(self) -> float:
        return 10**(-self.pkh)

    @property
    def ks(self) -> float:
        return 10**(-self.pks)

    @property
    def pka_nh4(self) -> float:
        '''NH4+ <--> NH3 + H+ , pKa = 9.24'''
        return 9.24

    @property
    def ka_nh4(self) -> float:
        '''NH4+ <--> NH3 + H+ , pKa = 9.24'''
        return 10**(-self.pka_nh4)

    @property
    def kb_nh3(self) -> float:
        '''NH3 + H2O <--> NH4+ + OH- , pKa = 4.76
        推导得到： Ka = Kw/Kb
        '''
        return self.kw / self.ka_nh4

    @property
    def water_dynamic_viscosity(self) -> float:
        '''
        Summary: 水的粘度与温度关系 ,Pa*s
        '''
        return get_water_dynamic_viscosity(self.temp)

    @property
    def temp_correction_factor(self) -> float:
        '''
        Summary: 温度补偿系数
        '''
        return get_temp_correction_factor(self.temp)
