# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 11:28:59 2013

@author: David Edwards
"""

from __future__ import division
from math import sqrt


def percent(x,y):
    return (float(x) / y) * 100


class Sample(object):
    
    """
    A class that takes a single data set as a list and defines basic 
    statistical properties of that data set.
    
    """
    
    def __init__(self, data_points):
        # try:         
        self.data_set = sorted(data_points)
        self.round_to = None
        # except TypeError:
        # self.data_set = sorted(list(data_points))
    
    def __str__(self):
        r = 'Sample of %s data points. \n' %len(self)
        r += 'Mean = %s \n' %round(self.mean(), 4)
        r += 'Stdev = %s' %round(self.stdev(), 4)
        return r
        
    def __len__(self):
        return len(self.data_set)
    
    def __iter__(self):
        return iter(self.data_set)
    
    def __getitem__(self, item):
        return self.data_set[item]
    
    def _round(self, n, **kwargs):
        try:
            if kwargs['raw']:
                return n
        except KeyError:
            if self.round_to is not None:
                n = round(n, self.round_to)
                if self.round_to == 0:
                    n = int(n)
        return n
    
    def round_to(self, dec_places):
        self.round_to = dec_places
        return 'Numerical answers will be \
                displayed with %s decimal places' %dec_places
    
    def mean(self, **kwargs):
        mean = float(sum(self.data_set)) / len(self)
        return self._round(mean, **kwargs)
    
    def median(self, **kwargs):
        """
        NOTE: This function includes all repeated values in the data set.
        
        n = the length of the data set.
        
        if n is odd: returns the middle element of the data set.
        if n is even: returns the mean of the two center elements.
        """
        n = len(self)
        if n % 2:
            median = self.data_set[n//2]    
        else:
            median = sum(self.data_set[n//2 - 1: n//2 + 1]) / 2. 
        return self._round(median, **kwargs)
    
    def variance(self, **kwargs):
        mean = self.mean(raw=True)
        sq_sums = float(sum([(x - mean)**2 for x in self.data_set]))
        variance = sq_sums / (len(self) - 1)   
        return self._round(variance, **kwargs)
    
    def stdev(self, **kwargs):
        stdev = sqrt(self.variance(raw=True))
        return self._round(stdev, **kwargs)
    
    def Q(self, q):
        """
        get the nth quartile 1 < n < 4
        
        """
        n = len(self)
        if q == 2:
            return self.median()
        elif q == 1:
            s = Sample(self.data_set[:n//2])
            return s.median()
        elif q == 3:
            if n % 2:
                s = Sample(self.data_set[n//2 + 1:])
                return s.median()
            s = Sample(self.data_set[n//2:])
            return s.median()
    
    def stats(self):
        stats = {
            'mean': round(self.mean(), 4),
            'median': round(self.median(), 4),
            'Q1 , Q3': (round(self.Q(1),4), round(self.Q(3), 4)),
            'variance': round(self.variance(), 4),
            'standard deviation': round(self.stdev(), 4),
        }
        return stats
        
    


