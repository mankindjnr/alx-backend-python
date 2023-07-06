#!/usr/bin/env python3
"""type-annotated function floor which takes a float n as argument and returns the floor of the float.

"""


def floor(n: float) -> int:
    """return the largest integer that is less that or equal to the float value"""
    integer, decimal = str(n).split(".")
    integer = int(integer)
    if (n > 0):
        return integer
    else:
        integer += - 1
        return integer
