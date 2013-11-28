# -*- coding: utf-8 -*-

from __future__ import division



def factorial(n):
    if n % 1 or n < 0:
        raise ValueError('n! is only defined for integers >= 0')
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


def nCk(n, k):
    numer = factorial(n)
    denom = factorial(k) * factorial(n - k)
    return numer / denom
