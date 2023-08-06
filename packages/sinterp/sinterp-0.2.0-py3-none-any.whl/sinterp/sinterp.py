# -*- coding: utf-8 -*-

from .config import ITERATION_SOLVER_SIZE_LIMIT, CHECK_INPUT
from .helpers import check_input1d, check_input2d, bisec_find_range


def interp1d(x: float, xp: list, yp: list, make_checks: bool = CHECK_INPUT) -> float:
    if make_checks:
        check_input1d(x, xp, yp)
    return interp1d_bisec(x, xp, yp) if len(xp) > ITERATION_SOLVER_SIZE_LIMIT else interp1d_iter(x, xp, yp)


def interp1d_iter(x: float, xp: list, yp: list):
    for ii in range(0, len(xp) - 1):
        if xp[ii] <= x <= xp[ii + 1]:
            return yp[ii] + ((x - xp[ii]) / (xp[ii + 1] - xp[ii])) * (yp[ii + 1] - yp[ii])
    return ValueError('Solution is not find')


def interp1d_bisec(x: float, xp: list, yp: list):
    i1, i2 = bisec_find_range(x, xp)
    return yp[i1] + ((x - xp[i1]) / (xp[i2] - xp[i1])) * (yp[i2] - yp[i1]) if i1 != i2 else yp[i1]


def interp2d(x: float, y: float, xp: list, yp: list, zp: list, make_checks: bool = CHECK_INPUT):
    if make_checks:
        check_input2d(x, y, xp, yp, zp)
    return interp2d_bisec(x, y, xp, yp, zp)


def interp2d_bisec(x: float, y: float, xp: list, yp: list, zp: list):
    i1, i2 = bisec_find_range(x, xp)
    j1, j2 = bisec_find_range(y, yp)
    z_j1 = zp[j1][i1] + ((x - xp[i1]) / (xp[i2] - xp[i1])) * (zp[j1][i2] - zp[j1][i1]) if i1 != i2 else zp[j1][i1]
    z_j2 = zp[j2][i1] + ((x - xp[i1]) / (xp[i2] - xp[i1])) * (zp[j2][i2] - zp[j2][i1]) if i1 != i2 else zp[j2][i1]
    return z_j1 + ((y - yp[j1]) / (yp[j2] - yp[j1])) * (z_j2 - z_j1) if j1 != j2 else z_j1
