
"""
I Threw this together and dont know if the stuff works

"""
from __future__ import division
from math import sqrt
from utils import nCk


class Distribution(object):
    
    def __init__(self):
        self.round_to = None
        
    def _(self, n, **kwargs):
        try:
            if kwargs['raw']:
                return n
        except KeyError:
            if self.round_to is not None:
                n = round(n, self.round_to)
                if self.round_to == 0:
                    n = int(n)
        return n
    

class DiscreteDistribution(Distribution):
    pass

class SampleProportion(DiscreteDistribution):
    
    def is_valid(self, n, p):
        return n * p >= 10 and n*(1 - p) > 10
    
    def mu(self, p):
        return p
    
    def variance(self, n, p, **kwargs):
            return self._((p*(1 - p)) / n, **kwargs)
    
    def stdev(self, n, p):
        return self._(sqrt(self.variance(n, p)))


class BinomialDistribution(DiscreteDistribution):
    
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.mu = self.n * self.p
        self.var = self.mu * (1 - self.p)
        self.stdev = sqrt(self.var)
        self.skewness = (1 - 2*self.p) / self.stdev
        super(BinomialDistribution, self).__init__()
    
    def pmf(self, k, **kwargs):
        n, p = self.n, self.p
        P = nCk(n,k)
        P *= (p**k) * (1-p)**(n-k)
        return self._(P, **kwargs)
    
    def cdf(self, k, **kwargs):
        n, p = self.n, self.p
        P = sum([self.pmf(i, raw=True) for i in xrange(int(k) + 1)])
        return self._(P, **kwargs)
    
class DiscreteUniformDistribution(DiscreteDistribution):
    
    def __init__(self, a, b):
        self.lowerbound = a
        self.upperbound = b
        self.n = self.upperbound - self.lowerbound
        self.p = 1 / self.n
        self.mu = (self.upperbound + self.lowerbound) / 2
        self.median = self.mu
        super(DiscreteUniformDistribution, self).__init__()
        

class NormalDistribution(Distribution):
    pass
