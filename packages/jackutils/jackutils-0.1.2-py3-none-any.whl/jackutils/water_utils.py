#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-05-08

'''
与Water相关的  Function
'''
from functools import lru_cache
from sympy import symbols, solve
import math
from typing import Any

'''
===================以下为线性公式，适合大量数据计算======================
格式 f(x)  : f_fx_x()
浓度单位默认都为mol/L
'''


def get_ion_strength(mmol_l: float, valence: float):
    '''
    Summary: 求单个离子ion strength
    para1  : mmol_l
    para2  : valence 价位
    '''
    return 0.5 * mmol_l/1000 * (valence**2)


def get_h_active(h: float = None,
                 h_active: float = None,
                 y1: float = None) -> float:
    if h_active:
        return h_active
    return h*y1


def ph_fx_h(h: float, y1: float = 1) -> float:
    '''
    Summary: h求ph
    '''
    return -math.log10(h*y1)


def h_mol_fx_ph(ph: float, y1: float = 1) -> float:
    '''
    Summary: 根据ph计算 h mol/L
    Note: 
        通过公式计算得到的为 h_active, 实际h需要考虑y1
    '''
    return 10**(-ph) / y1


def oh_mol_fx_ph(ph: float,
                 kw: float = 1e-14,
                 y1: float = 1) -> float:
    '''
    Summary: oh(ph)
        y1 为一价盐活度
    '''
    return kw/y1**2/(10**-ph)


@lru_cache(maxsize=128)
def h_mol_fx_A(A: float,
               kw: float = 1e-14,
               y1: float = 1) -> float:
    '''
    Summary: h(A) 根据 质子差值 计算 H mol/l
    Note   : ct=0,nt=0
        - y1 1加盐活度系数
    '''
    # kw = kw/y1**2
    A = A * y1
    if A >= 0:  # 酸性
        h = (-A+math.sqrt(A**2 - 4*-kw))/2 + A
    else:  # 碱性
        A = abs(A)
        oh = (-A+math.sqrt(A**2 - 4*-kw))/2 + A
        h = kw/oh
    return h/y1


def ph_fx_A(A: float,
            kw: float = 1e-14,
            y1: float = 1) -> float:
    '''
    Summary: ph(h_sub_oh_mol) 根据A 计算ph
    A= h_sub_oh_mol
        - y1 为1加盐活度系数
    '''
    h = h_mol_fx_A(A=A, kw=kw, y1=y1)
    return -math.log10(h)


def a0_fx_h_mol(h: float = None,
                h_active: float = None,
                k1: float = 4.168693834703355e-07,
                k2: float = 6.16595001861481e-11,
                y1: float = 1) -> float:
    '''
    Summary: a0(h)  # H2CO3 比例
        - 返回之前把h 转换为 h_active
    '''
    h = get_h_active(h=h, h_active=h_active, y1=y1)
    return (h**2) / (h**2 + k1 * h + k1 * k2)


def a1_fx_h_mol(h: float = None,
                h_active: float = None,
                k1: float = 4.168693834703355e-07,
                k2: float = 6.16595001861481e-11,
                y1: float = 1) -> float:
    '''
    Summary: a1(h)  # HCO3- 比例
    '''
    h = get_h_active(h=h, h_active=h_active, y1=y1)
    return (k1*h) / (h**2 + k1 * h + k1 * k2)


def a2_fx_h_mol(h: float = None,
                h_active: float = None,
                k1: float = 4.168693834703355e-07,
                k2: float = 6.16595001861481e-11,
                y1: float = 1) -> float:
    '''
    Summary: a2(h)  # CO3-2 比例
    '''
    h = get_h_active(h=h, h_active=h_active, y1=y1)
    return k1*k2 / (h**2 + k1 * h + k1 * k2)


def a0_fx_ph(ph: float,
             k1: float = 4.168693834703355e-07,
             k2: float = 6.16595001861481e-11) -> float:
    '''
    Summary: a0(ph)  # H2CO3 比例，无量纲
    '''
    h = 10**(-ph)  # 即为 h_active
    return (h**2) / (h**2 + k1 * h + k1 * k2)


def a1_fx_ph(ph: float,
             k1: float = 4.168693834703355e-07,
             k2: float = 6.16595001861481e-11) -> float:
    '''
    Summary: a1(ph)  # HCO3- 比例，无量纲
    '''
    h = 10**(-ph)  # 即为 h_active
    return (k1*h) / (h**2 + k1 * h + k1 * k2)


def a2_fx_ph(ph: float,
             k1: float = 4.168693834703355e-07,
             k2: float = 6.16595001861481e-11) -> float:
    '''
    Summary: a2(ph)  # CO3-2 比例，无量纲
    '''
    h = 10**(-ph)  # 即为 h_active
    return k1*k2 / (h**2 + k1 * h + k1 * k2)


def a_nh3_fx_ph(ph: float,
                ka_nh4: float = 5.754399373371567e-10) -> float:
    '''
    Summary: nh3(ph)  # NH3 比例，无量纲
    '''
    h = 10**(-ph)  # 即为 h_active
    return ka_nh4/(h+ka_nh4)


def a_nh4_fx_ph(ph: float,
                ka_nh4: float = 5.754399373371567e-10) -> float:
    '''
    Summary: nh4(ph)  # NH4+ 比例，无量纲
    '''
    h = 10**(-ph)  # 即为 h_active
    return h/(h+ka_nh4)


@lru_cache(maxsize=128)
def h_in_ct_k_fx_h_mol(h: float = None,
                       h_active: float = None,
                       kw: float = 1e-14,
                       k1: float = 4.168693834703355e-07,
                       k2: float = 6.16595001861481e-11,
                       y1: float = 1) -> float:
    '''
    Summary: h(A)，碳酸平衡中h  mol/l 占 ct 比例
    Note   : ct=0,nt=0
    '''
    a0 = a0_fx_h_mol(h=h, h_active=h_active, kw=kw, k1=k1, k2=k2, y1=y1)
    a1 = a1_fx_h_mol(h=h, h_active=h_active, kw=kw, k1=k1, k2=k2, y1=y1)
    return a0*2 + a1


def a_nh3_fx_h_mol(h: float = None,
                   h_active: float = None,
                   ka_nh4: float = 5.754399373371567e-10,
                   y1: float = 1) -> float:
    '''
    Summary: nh3(h)  # NH3-2 比例
    '''
    h = get_h_active(h=h, h_active=h_active, y1=y1)
    return ka_nh4/(h+ka_nh4)


def a_nh4_fx_h_mol(h: float = None,
                   h_active: float = None,
                   ka_nh4: float = 5.754399373371567e-10,
                   y1: float = 1) -> float:
    '''
    Summary: nh4(h)  # NH4+ 比例
    '''
    h = get_h_active(h=h, h_active=h_active, y1=y1)
    return h/(h+ka_nh4)


@lru_cache(maxsize=128)
def cal_h_balance_deviation(h: float,
                            A: float,  # 非活性
                            ct: float = 0,
                            nt: float = 0,
                            kw: float = 1e-14,
                            k1: float = 4.168693834703355e-07,
                            k2: float = 6.16595001861481e-11,
                            ka_nh4: float = 5.754399373371567e-10) -> float:
    '''
    Summary: 
        - 水中 h,A,ct,nt,kw,k1,k2,ka_nh4 具备 质子平衡，最终可以列出如下5次方程
        - 解方程消耗太大，因此可以反向进行求和
        - 用于 近似法求h_mol使得方程最接近0 (abs(result)<= 1e-7)
        - return 误差值(通过* 1e40放大）
    '''
    k3 = ka_nh4
    h = h
    # CT and NT ,5次方程
    x1 = k3+nt-A
    x2 = -kw-A*k3
    a = 1
    b = 2*ct+k1+x1
    c = 2*ct*k3 + k1*ct + k1*k2 + k1*x1 + x2
    d = k1*k3*ct + k1*k2*x1 + x2*k1 - kw*k3
    e = x2*k1*k2 - k1*k3*kw
    f = -k1*k2*k3*kw
    deviation = a*h**5 + b*h**4 + c*h**3 + d*h**2 + e*h + f
    return deviation*1e40


@lru_cache(maxsize=128)
def h_mol_fx_A_CT_NT(A: float,
                     ct: float = 0,
                     nt: float = 0,
                     kw: float = 1e-14,
                     k1: float = 4.168693834703355e-07,
                     k2: float = 6.16595001861481e-11,
                     ka_nh4: float = 5.754399373371567e-10) -> float:
    '''
    Summary: A, CT, NT 单位mol/L
    Note   : 最终要解1元3次方程，肯定有一个实数解
    Return :
    para1  : A : 总的 质子： h_in_ct + h_in_nt + [H]-[OH] mol/L
    para2  : ct: 总C  mol/L
    para3  : ct: 总NH3-NH4  mol/L
    '''
    k3 = ka_nh4
    h = symbols('h')
    # CT and NT ,5次方程
    x1 = k3+nt-A
    x2 = -kw-A*k3
    a = 1
    b = 2*ct+k1+x1
    c = 2*ct*k3 + k1*ct + k1*k2 + k1*x1 + x2
    d = k1*k3*ct + k1*k2*x1 + x2*k1 - kw*k3
    e = x2*k1*k2 - k1*k3*kw
    f = -k1*k2*k3*kw
    # 推导过程见照片
    ans = solve(
        a*h**5 + b*h**4 + c*h**3 + d*h**2 + e*h + f,
        h
    )
    # 取实数、正数解
    for x in ans:
        try:
            x = float(x)
            if x > 0:
                return x
        except:
            continue
    return None


@lru_cache(maxsize=128)
def h_mol_fx_A_CT_NT_binary(A: float,
                            ct: float = 0,
                            nt: float = 0,
                            kw: float = 1e-14,
                            k1: float = 4.168693834703355e-07,
                            k2: float = 6.16595001861481e-11,
                            ka_nh4: float = 5.754399373371567e-10) -> float:
    '''
    Summary: 二分法尝试计算
    Note   : 最高ph范围 = -2 - 16, h 范围 = 1e-16 ~ 1e-2 
    Return : h
    para1  : A : 总的 质子： h_in_ct + h_in_nt + [H]-[OH] mol/L
    para2  : ct: 总C  mol/L
    para3  : ct: 总NH3-NH4  mol/L
    '''
    h_range = range(-2, 17)
    h_res = None
    i_res = None
    # 先找到大的ph范围（1--10）**10**i，使 方程式正好为﹣
    # 在此基础上再找前缀
    # 此时前缀范围1-10能逐渐接近实际解
    for i in h_range:  # 极限19次
        h = 10**(-i)
        deviation = cal_h_balance_deviation(
            h=h, A=A, ct=ct, nt=nt, kw=kw, k1=k1, k2=k2, ka_nh4=ka_nh4)
        # print(f'1:i={i},h={h},deviation={deviation}')
        if deviation == 0:
            i_res = i
            h_res = h
            return h_res
        if deviation < 0:
            i_res = i
            h_res = h
            break

    start, end = 1, 10
    i = 0
    while i <= 15:  # 极限16次
        first = (start+end)/2
        h1 = first * h_res  # first * 1e-i
        deviation = cal_h_balance_deviation(
            h=h1, A=A, ct=ct, nt=nt, kw=kw, k1=k1, k2=k2, ka_nh4=ka_nh4)
        if deviation == 0:
            return h1
        elif deviation < 0:
            # 说明 first 太小
            start, end = first, end
        else:
            start, end = start, first
        i += 1
    return h1


@lru_cache(maxsize=128)
def h_mol_fx_A_CT(A: float,
                  ct: float = 0,
                  kw: float = 1e-14,
                  k1: float = 4.168693834703355e-07,
                  k2: float = 6.16595001861481e-11) -> float:
    '''
    Summary: A, CT 单位mol/L
    Note   : 最终要解1元4次方程
    Return :
    para1  : A : 总的 质子： h_in_h2co3 + [H]-[OH] mol/L
    para2  : ct: 总C  mol/L

    (-h_sub_oh+math.sqrt(h_sub_oh**2 - 4*-1e-14))/2 + h_sub_oh
    '''

    h = symbols('h')
    # CT, 4次方程
    a = 1
    b = 2*ct - A + k1
    c = k1*ct - kw - k1*A+k1*k2
    d = -k1*kw - k1*k2*A
    e = -k1*k2*kw
    # 推导过程见照片
    ans = solve(
        a*h**4 + b*h**3 + c*h**2 + d*h + e,
        h
    )
    # 取实数、正数解
    for x in ans:
        try:
            x = complex(x)
            if x.real > 0:
                return abs(x)
        except:
            continue
    return None


@lru_cache(maxsize=128)
def h_mol_fx_A_NT(A: float,
                  nt: float = 0,
                  kw: float = 1e-14,
                  ka_nh4: float = 5.754399373371567e-10) -> float:
    '''
    Summary: A, NT 单位mol/L，ct = 0 时候 求平衡 h
    Note   : 最终要解1元3次方程
    Return :
    para1  : A : 总的 质子： h_in_nt + [H]-[OH] mol/L
    para2  : nt: 总Nh3-NH4  mol/L

    (-h_sub_oh+math.sqrt(h_sub_oh**2 - 4*-1e-14))/2 + h_sub_oh
    '''
    k3 = ka_nh4
    h = symbols('h')
    # CT, 4次方程
    a = 1
    b = nt+k3-A
    c = -kw - A*k3
    d = -k3*kw
    # 推导过程见照片
    ans = solve(
        a*h**3 + b*h**2 + c*h + d,
        h
    )
    # 取实数、正数解
    for x in ans:
        try:
            x = complex(x)
            if x.real > 0:
                return abs(x)
        except:
            continue
    return None


@lru_cache(maxsize=128)
def get_h_mol_by_A_CT_NT(A: float,
                         ct: float = 0,
                         nt: float = 0,
                         kw: float = 1e-14,
                         k1: float = 4.168693834703355e-07,
                         k2: float = 6.16595001861481e-11,
                         ka_nh4: float = 5.754399373371567e-10) -> float:
    '''
    Summary: 根据不同情况 CT,NT 有零项时，选用4次或3次方程求解(严格按照解方程)
    Note   : 
    Return : h mol/L
    para1  : A : 总的 质子： h_in_ct + h_in_nt + [H]-[OH] (mol/L)
    para2  : ct: 总C  mol/L
    para3  : ct: 总NH3-NH4  mol/L
    '''
    if not ct and not nt:
        # 仅h，oh x**2
        return h_mol_fx_A(A=A, kw=kw)
    if ct and not nt:
        # h,oh,a0,a1,a2,x**4
        return h_mol_fx_A_CT(A=A, ct=ct, kw=kw, k1=k1, k2=k2)
    if not ct and nt:
        # h,oh,a0,a1,a2,x**3
        return h_mol_fx_A_NT(A=A, nt=nt, kw=kw, ka_nh4=ka_nh4)
    if ct and nt:
        # h,oh,a0,a1,a2,a_nh3,a_nh4,x**5
        return h_mol_fx_A_CT_NT(A=A, ct=ct, nt=nt, kw=kw, k1=k1, k2=k2, ka_nh4=ka_nh4)


@lru_cache(maxsize=128)
def get_h_mol_by_A_CT_NT_binary(A: float,
                                ct: float = 0,
                                nt: float = 0,
                                kw: float = 1e-14,
                                k1: float = 4.168693834703355e-07,
                                k2: float = 6.16595001861481e-11,
                                ka_nh4: float = 5.754399373371567e-10) -> float:
    '''
    Summary: 根据不同情况 CT,NT 有零项时，选用4次或3次方程求解(二分法)
    Note   : 
    Return : h mol/L
    para1  : A : 总的 质子： h_in_ct + h_in_nt + [H]-[OH] (mol/L)
    para2  : ct: 总C  mol/L
    para3  : ct: 总NH3-NH4  mol/L
    '''
    if not ct and not nt:
        # 仅h，oh x**2
        return h_mol_fx_A(A=A, kw=kw)
    else:
        return h_mol_fx_A_CT_NT_binary(A=A, ct=ct, nt=nt, kw=kw, k1=k1, k2=k2, ka_nh4=ka_nh4)


def get_osp(mmol_l: float, temp: float = 25) -> float:
    '''
    Summary: 渗透压计算
    '''
    return mmol_l * 8.314 * (temp + 273.15) / 100000
