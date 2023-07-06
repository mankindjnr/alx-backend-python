#!/usr/bin/env python3
def floor(n: float) -> int:
    """return the largest integer that is less that or equal to the float value"""
    integer, decimal = str(n).split(".")
    integer = int(integer)
    if (n > 0):
        return integer
    else:
        integer += - 1
        return integer
