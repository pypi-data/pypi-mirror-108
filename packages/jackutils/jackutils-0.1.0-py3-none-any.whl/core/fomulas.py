#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-05-02

'''
Summary: 物理公式及计算
** 仅复杂计算采用lru_cache
'''
from typing import List
import math
from functools import lru_cache
# app
from . import const


@lru_cache(maxsize=128)
def get_round_area(diameter: float) -> float:
    '''直径计算圆面积'''
    return (diameter/2)**2*const.PI


@lru_cache(maxsize=128)
def get_round_radius(area: float) -> float:
    '''获得半径'''
    return (area/const.PI)**(1/2)


@lru_cache(maxsize=128)
def get_round_diameter(area: float) -> float:
    '''面积计算圆直径'''
    return (area/const.PI)**(1/2)*2


@lru_cache(maxsize=128)
def get_round_tank_size(volumn: float, height_diameter: float = 1.2) -> dict:
    '''
    根据有效体积V，超高H_add,高径比(有效高度:直径) 计算size
    '''
    # diameter = height / height_diameter
    # R = diameter/2 = height/height_diameter/2
    # area = R**2*const.PI
    # area = (height/height_diameter/2)**2 * const.PI
    # volumn = area * height = (height/height_diameter/2)**2 * const.PI * height
    # height**3 = volumn / const.PI * (height_diameter*2)**2
    height = (volumn / const.PI * (height_diameter*2)**2)**(1/3)
    diameter = height/height_diameter
    return {'height': height, 'diameter': diameter}


@lru_cache(maxsize=128)
def get_round_tank_height(volumn: float, diameter: float) -> float:
    '''根据V,D得到H'''
    area = get_round_area(diameter=diameter)
    return volumn/area


@lru_cache(maxsize=128)
def get_round_tank_volumn(height: float, diameter: float) -> float:
    '''根据D，H获得 圆形槽体V'''
    return height*(diameter/2)**2*const.PI


@lru_cache(maxsize=128)
def get_v_round_pip(m3ph: float, diameter: float) -> float:
    '''
    Summary: 圆管计算流速
    Params:
        - q: 流量 m3/h 
        - diameter: 直径 m
        return 单位m/s
    '''
    s = get_round_area(diameter=diameter)
    return m3ph / s / 3600


@lru_cache(maxsize=128)
def get_temp_correction_factor(temp: float) -> float:
    '''
    Summary: 温度补偿系数计算
        采用国际水和水蒸气性质协会(IAPWS)官方公式
        DOW也采用此公式作为温度补偿计算
    '''
    k = temp+273.15  # 热力学温度
    kk = k/300
    a1 = 280.68*(kk**(-1.9))
    a2 = 511.45*(kk**(-7.7))
    a3 = 61.131*(kk**(-19.6))
    a4 = 0.45903*(kk**(-40))
    return 890/(a1+a2+a3+a4)


def get_hydro_d(area: float, perimeter: float) -> float:
    '''
    Summary: 根据 截面积 和 湿润周长，计算 水力直径（计算re）
    '''
    return area*4 / perimeter


@lru_cache(maxsize=128)
def get_water_viscosity(temp: float) -> float:
    '''
    Summary: 计算 水的粘度 N·s/㎡ = Pa*s
    '''
    t = temp  # + 273.15
    return 0.001779/(1+0.03368*t+0.0002210*t**2)


@lru_cache(maxsize=128)
def get_water_dynamic_viscosity(temp: float) -> float:
    '''
    Summary: 根据 温度 计算 水的 运动粘度
    单位: Pa*s 
    '''
    return 0.001779 / (1+0.03368*temp+0.0002210*temp**2)


@lru_cache(maxsize=128)
def get_water_kinematic_viscosity(temp: float) -> float:
    '''
    Summary: 根据 温度 计算 水的 运动粘度
    单位: Pa*s 
    '''
    dynamic_viscosity = 0.001779 / (1+0.03368*temp+0.0002210*temp**2)
    density = 997
    return dynamic_viscosity / density


def get_re(d: float,  # 4倍面积/润湿的周长
           v: float,
           density_kg_m3: float = 997,  # 密度 kg/m3
           dynamic_viscosity: float = None,  # 动力粘度 Pa*s
           kinematic_viscosity: float = 1.006e-6  # 运动粘度 m2/s
           ) -> float:
    '''
    Summary: 雷诺数计算 Reynolds number
        - Re=ρvd/η (1)
        - d: 定型尺寸 m (圆管为直径) 
        - ρ：density 密度25℃水为997, kg/m3
        - v: 流速 m/s 
        - η: dynamic_viscosity 动力粘度 Pa*s 或 kg/(m*s) 或 N·s/㎡:
            在流体中取两面积各为1m2，相距1m，
            相对移动速度为1m/s时所产生的阻力称为动力粘度。
            单位Pa.s（帕.秒） [2]  。
            过去使用的动力粘度单位为泊或厘泊，泊（poise）或厘泊为非法定计量单位。
            20℃时水的运动黏度ν=1.006×10^(-6) (m2/s)
        - υ:kinematic_viscosity (m2/s)
            - η＝ρυ -> η = kg/m3 * m2/s = kg/(m*s) = Pa·s 即动力粘度的单位
                - 压强的定义Pa=N/m^2,
                - Pa*s=N*s/m^2
                - 牛顿第二定律N=kg*m/s^2,
                - 所以 Pa*s=(kg*m/s^2)*s/m^2=kg/(m*s)
        - 式中的动力粘度η用运动粘度υ来代替，因η＝ρυ, 因此 Re = vd/υ (2)#
            - Re = 流速*定型尺寸/运动粘度 
            - η＝ρυ -> η = kg/m3 * m2/s = kg/(m*s) = Pa·s 即动力粘度的单位
            - η/ρ＝υ
    Params:
        - d: 定型尺寸 m (圆管为直径)
        - v: 流速 m/s 
        - density_kg_m3: 密度 kg/m3
        - dynamic_viscosity: 动力粘度, Pa·s， 25℃水=0.89e-3 Pa·s (kg/(m·s))
        - kinematic_viscosity: 运动粘度, m2/s,25℃时水的运动粘度0.893e-6 (m2/s)
    Unit:
        - m * m/s / (m2/s) = 无量纲
        - m * m/s * kg/m3 / (kg/(m*s)) => kg/m/s / (kg/m/s) -> 1 
    '''
    if kinematic_viscosity:
        # 运动粘度计算
        return d*v/kinematic_viscosity
    # 粘度计算
    return d*v*density_kg_m3 / dynamic_viscosity


def get_re_water(d: float, v: float, temp: float):
    '''
    Summary: 水的 雷诺数
    '''
    dynamic_viscosity = get_water_dynamic_viscosity(temp=temp)
    return get_re(d=d, v=v, dynamic_viscosity=dynamic_viscosity)


def get_dp_hazen_williams_law(re: float, v_m_s: float, d_m: float, length_m: float) -> float:
    '''
    Summary: Hazen williams law
            ---H=10.67 * 121**-1.85 * D**-4.87 * Q*1.85 L 121指PVC管道的表面粗糙度常数

            hf = ru *(l/D)*(v^2/2/g)
            - ru: 沿程阻力系数
            - l :管道长度 m
            - D : 管道内径 m, 用水力半径替代
            - v : 平均流速 m/s
            - g : 重力加速度 m/s2
    '''
    # 返回为 bar 单位
    g = 9.801
    if re < 2320:
        ru = 64/re
    elif 3000 < re < 10e5:
        ru = 0.3164*re**(-0.25)
    else:
        ru = 0.308*(0.842-math.log(re))**-2
    return ru*length_m/d_m*v_m_s**2/(2*g) / 10


@lru_cache(maxsize=128)
def debye_huckel(ion_strength: float = 0, valence: float = 1) -> float:
    '''
    Summary: 德拜-休克尔公式：适用于【强电解质】【稀溶液】的活度计算经验公式
            25℃，A=0.509(mol/kg)**(-0.5)
    Note   : lnx= -A * zi**2 * I**0.5
    Return : ya
    para1: ion_strength: 离子强度
    para2: valence:离子价位
    '''
    i = ion_strength
    # res = (math.e)**(-0.509*valence**2 *
    #                  i**0.5)
    res = (math.e)**(-0.509*valence**2 * (i**0.5/(1+i**0.5)-0.3*i))
    return round(res, 3)
