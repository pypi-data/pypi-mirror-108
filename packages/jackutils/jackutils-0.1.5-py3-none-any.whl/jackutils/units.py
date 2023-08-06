#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-03-06


'''
单位换算 类
'''

import copy
import numbers
from dataclasses import dataclass, InitVar
from pydantic import BaseModel

# 单位换算
# 非公制全部为美制
UNIT_DB = {
    'length': {
        'm': 1,
        'dm': 10,
        'cm': 100,
        'mm': 1000,
        'km': 0.001,
        'um': 1e6,
        'inch': 39.370079,
        'foot': 3.2808399,
        'ft': 3.2808399,
        'mile': 0.00062137119,  # 英里
        'yard': 1.0936133,
        'mil': 39370.079,       # 毫英寸  1inch = 1000 mil
        '米': 1,
        '分米': 10,
        '厘米': 100,
        '毫米': 1000,
        '千米': 0.001,
        '微米': 1e6,
        '英寸': 39.370079,
        '英尺': 3.2808399,
        '英里': 0.00062137119,
        '码': 1.0936133,
        '毫英寸': 39370.079
    },
    'area': {  # {f'{k}2':v**2 for k, v in le.items()}
        'm2': 1,
        'dm2': 100,
        'cm2': 10000,
        'mm2': 1000000,
        'km2': 1e-06,
        'um2': 1000000000000.0,
        'inch2': 1550.0031204662407,
        'in2': 1550.0031204662407,
        'foot2': 10.76391044943201,
        'ft2': 10.76391044943201,
        'mile2': 3.861021557620161e-07,
        'yard2': 1.1959900499368898,
        'mil2': 1550003120.466241,
        '平方米': 1,
        '平方分米': 100,
        '平方厘米': 10000,
        '平方毫米': 1000000,
        '平方千米': 1e-06,
        '平方微米': 1000000000000.0,
        '平方英寸': 1550.0031204662407,
        '平方英尺': 10.76391044943201,
        '平方英里': 3.861021557620161e-07,
        '平方码': 1.1959900499368898
    },
    'volume': {  # {f'{k}3':v**3 for k, v in le.items()}
        'm3': 1,
        'dm3': 1000,
        'l': 1000,
        'dl': 100,  # 10升
        'liter': 1000,
        'cm3': 1000000,
        'mm3': 1000000000,
        'km3': 1e-09,
        'um3': 1e+18,
        'inch3': 61023.74530300241,
        'in3': 61023.74530300241,
        'foot3': 35.314666882523476,
        'ft3': 35.314666882523476,
        'mile3': 2.399127559874093e-10,
        'yard3': 1.3079506252786468,
        'mil3': 61023745303002.414,
        'gal': 264.1720524,  # 美制加仑
        'g': 264.1720524,  # 美制加仑
        'gallon': 264.1720524,  # 美制加仑
        'qt': 1056.6882094,  # 美制夸脱
        'quart': 1056.6882094,  # 美制夸脱
        'bbl': 6.2898108,  # 美制桶（42gal）
        'barrel': 6.2898108,  # 美制桶（42gal）
        'pt': 2113.3764189,
        'pint': 2113.3764189,
        '立方米': 1,
        '升': 1000,
        '十升': 100,
        '立方分米': 1000,
        '立方厘米': 1000000,
        '立方毫米': 1000000000,
        '立方千米': 1e-09,
        '立方微米': 1e+18,
        '立方英寸': 61023.74530300241,
        '立方英尺': 35.314666882523476,
        '立方英里': 2.399127559874093e-10,
        '立方码': 1.3079506252786468,
        '加仑': 264.1720524,  # 美制加仑
        '品脱': 2113.3764189,
        '夸脱': 1056.6882094,  # 美制夸脱
        '桶': 6.2898108,  # 美制桶（42gal）

    },
    'time': {  # d会涉及到 hr_per_d尽量不用
        'h': 1,
        'hour': 1,
        'hours': 1,
        'm': 60,
        'min': 60,
        'minute': 60,
        'minutes': 60,
        's': 3600,
        'second': 3600,
        'seconds': 3600,
        'd': 1/24,
        'day': 1/24,
        'days': 1/24,
        '小时': 1,
        '分钟': 60,
        '秒': 3600,
        '天': 1/24,
        '日': 1/24,
    },
    'weight': {
        'kg': 1,
        '千克': 1,
        '公斤': 1,
        'g': 1e3,
        '克': 1e3,
        'mg': 1e6,
        '毫克': 1e6,
        'ton': 0.001,
        '吨': 0.001,
        'lb': 2.2046226,
        '磅': 2.2046226,
        'cwt': 0.022046226,  # 美担(cwt)
        '美担': 0.022046226,  # 美担(cwt)
        'cwt uk': 0.019684131,  # 英担(cwt)
        '英担': 0.019684131,  # 英担(cwt)
        'dr': 564.38339,
        'oz': 35.273962,
        '两': 20,
        '斤': 2,
        '担': 0.02,
        '钱': 200,
        'ct': 5000,
        '克拉': 5000,
        'gr': 2e4,
        '格令': 2e4,
        'point': 5e5,
        '分': 5e5,
        'oz': 32.15074254,
        '盎司': 32.15074254
    },
    'velocity': {  # 速度
        'm/s': 1,
        'm/min': 60,
        'm/h': 3600,
        'km/h': 3.6,
        '米/秒': 1,
        '米/分钟': 60,
        '米/小时': 3600,
        '千米/小时': 3.6,
        'mile/h': 2.23693629,
        '英里/时': 2.23693629,
        'ft/s': 472.44094488,
        '英尺/秒': 472.44094488,
        'in/s': 39.37007874,
        '英寸/秒': 39.37007874,
        'c': 3.33564095e-9,
        '光速': 3.33564095e-9,
        'mach': 0.00293858,
        '马赫': 0.00293858,
    },
    'flow': {  # 流量
        'm3/h': 1,
        't/h': 1,
        'm3ph': 1,
        'm3/d': 24,
        'm3pd': 24,
        'l/h': 1000,
        'lph': 1000,
        'liter/h': 1000,
        'l/min': 1000/60,
        'liter/min': 1000/60,
        'lpm': 1000/60,
        'l/s': 1000/3600,
        'liter/s': 1000/3600,
        'm3/min': 1/60,
        'm3/s': 1/3600,
        'gallon/min': 1*264.1720524/60,
        'gal/min': 1*264.1720524/60,
        'gpm': 1*264.1720524/60,
        'gal/h': 1*264.1720524,  # gph
        'gallon/h': 1*264.1720524,  # gph
        'gph': 1*264.1720524,  # gph
        'gallon/day': 1*264.1720524/60*24*60,  # 按照24小时算
        'gal/day': 1*264.1720524/60*24*60,
        'gpd': 1*264.1720524/60*24*60,
        # 中文
        '立方米/小时': 1,
        '吨/小时': 1,
        '吨/天': 24,
        '升/小时': 1000,
        '升/分钟': 1000/60,
        '升/秒': 1000/3600,
        '立方米/分钟': 1/60,
        '立方米/秒': 1/3600,
        '加仑/分钟': 1*264.1720524/60,
        '加仑/小时': 1*264.1720524,  # gph
        '加仑/天': 1*264.1720524/60*24*60,  # 按照24小时算
    },
    'power': {
        # 功率
        'kw': 1,
        'w': 1000,
        'hp': 1.341,  # 英制马力 HP
        'ps': 1.36,  # 米制马力
        'j/s': 1000,  # 焦耳/秒
        'kg·m/s': 102,  # 公斤·米/秒
        'kcal/s': 0.239,  # 千卡/秒
        '千瓦': 1,
        '瓦': 1000,
        '英制马力': 1.341,  # 英制马力 HP
        '米制马力': 1.36,  # 米制马力
        '焦耳/秒': 1000,  # 焦耳/秒
        '公斤·米/秒': 102,  # 公斤·米/秒
        '千卡/秒': 0.239,  # 千卡/秒
        'j/h': 3.6e6,
        '焦耳/小时': 3.6e6,
        'kgf·m/s': 101.9716213,
        '千克力·米/秒': 101.9716213,
        'cal/s': 239.00000105,
        '卡/秒': 239.00000105,
        'hp': 1.35962162,
        '米制马力': 1.35962162,
        'ft*lb/s': 737.56217557,
        '英尺*磅/秒': 737.56217557,
        'n*m/s': 1000,
        '牛顿*米/秒': 1000
    },
    'pressure': {
        # 压力
        'bar': 1,
        '巴': 1,
        'head': 10,
        'h': 10,
        '扬程': 10,
        'pa': 1e5,
        '帕斯卡': 1e5,
        '帕': 1e5,
        'n/m2': 1e5,
        '牛顿/平方米': 1e5,
        'hpa': 1,
        '百帕': 1,
        'kpa': 100,
        '千帕': 100,
        'mpa': 0.1,
        '兆帕': 0.1,
        'atm': 0.98692327,
        '标准大气压': 0.98692327,
        'lbf/ft2': 2088.5435,
        'lbf/in2': 14.503774,
        '磅力/英寸': 14.503774,
        'psi': 14.503774,
        '磅力/平方英寸': 14.503774,
        'in hg': 29.529988,
        'kgf/cm2': 1.0197162,
        '公斤力/平方厘米': 1.0197162,
        'kgf/m2': 10197.162,
        '公斤力/平方米': 10197.162,
        'mmh2o': 10197.2,
        '毫米水柱': 10197.2,
        'mh2o': 10197.2*1e-3,
        '米水柱': 10197.2*1e-3,
        'torr': 750.06168,
        '托': 750.06168,
        'mmhg': 750.06168282,
        '毫米汞柱': 750.06168282,
    },
    'density': {
        # 密度
        'g/cm3': 1,
        '克/立方厘米': 1,
        'kg/l': 1,
        '千克/升': 1,
        'ton/m3': 1,
        '吨/立方米': 1,
        'kg/dm3': 1,
        '千克/立方分米': 1,
        'kg/m3': 1000,
        '千克/立方米': 1000,
        'lb/gal': 8.34543421,
        'lb/gallon': 8.34543421,
        '磅/加仑': 8.34543421,
        '磅/美加仑': 8.34543421,
        'lb/ft3': 62.42197253,
        '磅/立方英尺': 62.42197253,
        'lb/in3': 0.0361273,
        'lb/inch3': 0.0361273,
        '磅/立方英寸': 0.0361273
    },
    'dynamic viscosity': {
        'pa*s': 1,
        '帕斯卡*秒': 1,
        'kg/(m*s)': 1,
        '千克/(米*秒)': 1,
        'mpa*s': 1000,
        '毫帕斯卡*秒': 1000,
        'p': 10,
        '泊': 10,
        'cp': 1000,
        '厘泊': 1000,
        'kgf*s/m2': 0.10197162,
        'lbf*s/ft2': 0.02088542,
        '磅力秒每平方英尺': 0.02088542,
        'lb/(ft*h)': 2419.08756855,
    },
    'kinematic viscosity': {
        'm2/s': 1,
        '平方米/秒': 1,
        'st': 1e4,
        '斯': 1e4,
        'cst': 1e6,
        '厘斯': 1e6,
        'cm2/s': 1e4,
        '平方厘米/秒': 1e4,
        'mm2/s': 1e6,
        '平方毫米/秒': 1e6,
        'ft2/s': 10.76391505,
        '平方英尺/秒': 10.76391505
    },
    'force': {
        'n': 1,
        '牛顿': 1,
        'lbf': 0.22480892,
        '磅力': 0.22480892,
        'dyn': 1e5,
        '达因': 1e5,
        'kgf': 0.10197162,
        '千克力': 0.10197162,
        'gf': 101.9716213,
        '克力': 101.9716213,
        'tf': 1.01971621e-4,
        '公吨力': 1.01971621e-4,
    },
    'flux': {
        'lmh': 1,
        'l/(m2*h)': 1,
        '升/(平方米*小时)': 1,
        'm3/(m2*d)': 0.024,
        'gfd': 0.5890172802333705,
        'gal/(ft2*d)': 0.5890172802333705,
        '加仑/(平方英尺*天)': 0.5890172802333705,
    },
    # 浓度 摩尔质量/体积
    'concentration mol volume': {
        'mol/l': 1,
        '摩尔/升': 1,
        'mmol/l': 1000,
        '毫摩尔/升': 1000,
        'ppm_caco3': 1e5
    },
    # 浓度 质量/体积
    'concentration weight volume': {
        'mg/l': 1,
        '毫克/升': 1,
        'g/l': 1e-3,
        '克/升': 1000,
        'kg/m3': 1e-3,
        '千克/立方米': 1e-3,
        'g/m3': 1e-6,
        '克/立方米': 1e-6
    },
    # 浓度 质量/质量 (比例)
    'percentage': {
        'ppm': 1,  # part per million
        'ppb': 1e3,  # part per billion 
        'ppt': 1e6,  # part per trillion 
        'wt': 1e-4  # 百分比
    }
}

SUPPORT_UNITS = {
    'length': '长度',
    'area': '面积',
    'volume': '体积',
    'time': '时间',
    'weight': '重量',
    'velocity': '速度',
    'flow': '流量',
    'power': '功率',
    'pressure': '压力',
    'density': '密度',
    'dynamic viscosity': '动力粘度',
    'kinematic viscosity': '运动粘度',
    'force': '力',
    'flux': '水通量'
}


@dataclass
class UnitMixin():
    '''
    Summary: 单位换算基础class 
    Note   : 实现加减乘除
    Example: 获得in2 UnitArea(10,'m2').get('in2')
    '''
    val: float = 0
    unit: str = None  # 用来查询
    __unittype__ = ''
    unittype: InitVar[str] = None

    def __post_init__(self, unittype):
        self.unit = str(self.unit).lower()
        if not self.__unittype__ and unittype:
            # 赋值
            self.__unittype__ = unittype
        if not self.unit or not self.unit in self.unitdt:
            raise Exception(f'[{self.unit}] not in {self.__unittype__} range')

    @property
    def unitdt(self):
        '''
        Summary: 获得 单位换算 list
        '''
        return UNIT_DB.get(self.__unittype__, {})

    @property
    def base_unit(self):
        '''
        Summary: 基准单位
        '''
        dt = self.unitdt
        for x in dt:
            if dt[x] == 1:
                return x
        raise Exception(f'{self.__unittype__}没有找到基准单位')

    @property
    def base_unit_val(self):
        '''
        Summary: 基准单位 值
        '''
        return self.val / self.unitdt.get(self.unit)

    def get(self, unit: str, rd: int = None) -> numbers.Real:
        '''
        Summary: 获得特定unit的结果
        params: 
            - unit 需要的单位
            - rd round的位数
        '''
        unit_lower = str(unit).lower()

        if unit_lower == self.unit:
            val = self.val
        else:
            if not unit_lower or not unit_lower in self.unitdt:
                raise Exception(f'[{unit}] not in {self.__unittype__} range')
            val = self.base_unit_val * self.unitdt.get(unit_lower)
        if isinstance(rd, int) and rd >= 0:
            return round(val, rd)
        return val

    def __call__(self, unit: str = None):
        return self.get(unit)

    def get_str(self, unit: str, rd: int = 0, use_standard_unit: bool = False) -> str:
        '''
        Summary: 获得str 表示的结果
        params: 
            - unit 需要的单位
            - rd round的位数
            - use_standard_unit 是否采用标准单位(lower传入的单位str)，不然就保持传入的大小写展示
        '''
        val = self.get(unit=unit)
        if use_standard_unit:
            unit = str(unit).lower()
        if not rd:
            return f'{val} {unit}'
        return f'{round(val,rd)} {unit}'

    def reset_unit(self, unit: str):
        '''
        Summary: 将 self unit设置为指定unit，同时改变val值
        '''
        val = self.get(unit=unit)
        self.val = val
        self.unit = unit

    @property
    def all_units(self):
        '''
        Summary: 所有支持的单位数据
        '''
        base = self.base_unit_val
        return {k: v*base for k, v in self.unitdt.items()}

    def __mul__(self, i: numbers.Number):
        '''
        Summary: 乘法
        '''
        new = copy.deepcopy(self)
        try:
            i = float(i)
            if i < 0:
                raise ValueError(f'i 必须>=0才能*UnitMixin, 目前为{i}')
            new.val *= i
            return new
        except:
            raise ValueError(f'i 必须>=0才能*UnitMixin, 目前为{i}')

    def __truediv__(self, i: numbers.Number):
        '''
        Summary: 除法
        '''
        new = copy.deepcopy(self)
        try:
            i = float(i)
            if i <= 0:
                raise ValueError(f'i 必须>0才能 UnitMixin/i, 目前为{i}')
            new.val /= i
            return new
        except:
            raise ValueError(f'i 必须>0才能 UnitMixin/i, 目前为{i}')

    def __add__(self, other):
        '''
        Summary: 同类相加
        '''
        if not isinstance(other, self.__class__):
            raise TypeError('UnitMixin仅限相同单位类型相加(如长度只能和长度相加)')
        new = self.__class__()  # 默认配置
        new.val = self.get(new.unit) + other.get(new.unit)
        return new

    def __sub__(self, other):
        '''
        Summary: 同类相减
        '''
        if not isinstance(other, self.__class__):
            raise TypeError('UnitMixin仅限相同单位类型相减(如长度只能和长度相减)')
        new = self.__class__()  # 默认配置
        new.val = self.get(new.unit) - other.get(new.unit)
        return new


@dataclass
class UnitLength(UnitMixin):
    val: float = 0
    unit: str = 'm'
    __unittype__ = 'length'


@dataclass
class UnitArea(UnitMixin):
    val: float = 0
    unit: str = 'm2'
    __unittype__ = 'area'


@dataclass
class UnitVolume(UnitMixin):
    val: float = 0
    unit: str = 'm3'
    __unittype__ = 'volume'


@dataclass
class UnitWeight(UnitMixin):
    val: float = 0
    unit: str = 'kg'
    __unittype__ = 'weight'


@dataclass
class UnitTime(UnitMixin):
    val: float = 0
    unit: str = 'h'
    __unittype__ = 'time'


@dataclass
class UnitVelocity(UnitMixin):
    val: float = 0
    unit: str = 'm/s'
    __unittype__ = 'velocity'


@dataclass
class UnitFlow(UnitMixin):
    val: float = 0
    unit: str = 'm3/h'
    __unittype__ = 'flow'


@dataclass
class UnitPower(UnitMixin):
    val: float = 0
    unit: str = 'kw'
    __unittype__ = 'power'


@dataclass
class UnitPressure(UnitMixin):
    val: float = 0
    unit: str = 'bar'
    __unittype__ = 'pressure'


@dataclass
class UnitDensity(UnitMixin):
    val: float = 0
    unit: str = 'kg/l'
    __unittype__ = 'density'


@dataclass
class UnitDynamicViscosity(UnitMixin):
    val: float = 0
    unit: str = 'kg/(m*s)'
    __unittype__ = 'dynamic viscosity'


@dataclass
class UnitKinematicViscosity(UnitMixin):
    val: float = 0
    unit: str = 'm2/s'
    __unittype__ = 'kinematic viscosity'


@dataclass
class UnitConcentrationMolVolume(UnitMixin):
    val: float = 0
    unit: str = 'mol/l'
    __unittype__ = 'concentration mol volume'


@dataclass
class UnitConcentrationWeightVolume(UnitMixin):
    val: float = 0
    unit: str = 'mg/l'
    __unittype__ = 'concentration weight volume'


@dataclass
class UnitPercentage(UnitMixin):
    val: float = 0
    unit: str = 'ppm'
    __unittype__ = 'percentage'


'''
============================= 以下为pd =================================
'''


class UnitPd(BaseModel):
    '''
    Summary: 标准单位接口格式
    '''
    val: float = 0
    unit: str = ''

    class Config:
        orm_mode = True
