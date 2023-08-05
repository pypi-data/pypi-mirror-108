#!/usr/bin/env python3
# coding: utf-8

from math import *


def filletByReduce(
        angle: float,
        reduce: float
) -> float:
    return reduce * tan(angle / 2)


def reduceByFillet(
        angle: float,
        fillet: float
) -> float:
    return fillet / tan(angle / 2)


if __name__ == '__main__':
    print(filletByReduce(pi/2, 1.0))
    print(reduceByFillet(pi/2, 1.0))
    print(filletByReduce(pi/4, 1.0))
    print(reduceByFillet(pi/4, 1.0))
