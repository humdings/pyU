from __future__ import division
from math import log10, floor


def tIntegral(f, a, b, n=10000):
    """
    Approximates the definite integral of f from a to b by
    the composite trapezoidal rule, using n subintervals
    """
    s = (b - a) / n
    I = (.5*(f(a) + f(b)) + sum(f(a + i*s) for i in xrange(1,n))) * s
    return I 


def sIntegral(f, a, b, n=10000):
    """
    Approximates the definite integral of f from a to b by
    the composite Simpson's rule, using n subintervals
    """
    s = (b - a) / n 
    I = sum(4*f(a + i*s) for i in xrange(1, n, 2))
    I += sum(2*f(a + i*s) for i in xrange(2, n-1, 2))
    return s * (f(a) + f(b) + I) / 3.


def sig_figs(x, sigfigs=5):
    ''' Rounds x to a number of sigfigs '''
    if x == 0:
        return 0
    sign = x / abs(x)
    x = abs(x)
    return round(x, sigfigs-int(floor(log10(x)))-1) * sign
