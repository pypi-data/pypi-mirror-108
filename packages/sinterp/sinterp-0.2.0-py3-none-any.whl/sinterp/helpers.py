# -*- coding: utf-8 -*-


def bisec_find_range(k: float, kp: list):
    k1, k2 = [0, len(kp) - 1]
    while k2 - k1 > 1:
        _ = int((k2 + k1) / 2)
        if k == kp[k1]:
            return k1, k1
        elif k == kp[k2]:
            return k2, k2
        elif kp[k1] < k < kp[_]:
            k2 = _
        elif kp[_] < k < kp[k2]:
            k1 = _
        else:
            return _, _
    return k1, k2


def check_input1d(x: float, xp: list, yp: list):
    check_list1d_range(x, xp)
    if len(yp) < 2:
        raise ValueError('list should have minimum two items')
    if len(xp) != len(yp):
        raise ValueError('lists should have same length')


def check_input2d(x: float, y: float, xp: list, yp: list, zp: list):
    check_list1d_range(x, xp)
    check_list1d_range(y, yp)
    check_list2d_size(xp, yp, zp)


def check_list1d_range(v: float, vp: list):
    if v < vp[0] or v > vp[-1]:
        raise ValueError('value is out of interpolation range')
    if len(vp) < 2:
        raise ValueError('list should have minimum two items')


def check_list2d_size(xp: list, yp: list, zp: list):
    if len(yp) != len(zp):
        raise ValueError('lists should have same length')
    for row in zp:
        if len(row) != len(xp):
            raise ValueError('lists should have same length')
