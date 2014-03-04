# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 19:59:09 2013

@author: David Edwards
"""

from pyU.linalg.matrix import Matrix


def least_squares(data, deg=1):
    """
    Uses Normal equation  xTxA = xTy to solve for the coefficients
    of least squares. Returns polynomial coefficients, residuals, and r^2 error
    
    pass data as either [(x1,y1),..(xn,yn)] tuples or
    [[x_points], [y_points]]
    """
    if len(data) == 2:
        data = zip(data[0], data[1])
    d = deg + 1
    y = Matrix([[x[1] for x in data]]).transpose()
    x = Matrix([[x[0]**j for x in data] for j in xrange(d)]).transpose()
    xTx = x.transpose() * x
    xTy = x.transpose() * y
    A = xTx.solve(xTy)
    y_hat = x * Matrix(A._as_col)
    residual = y - y_hat
    err = residual.transpose() * residual     
    return A, residual ,err[0][0]


class OLS(object):
    
    '''
    Ordinary Least squares regression for polynomial fitting. 
    '''
    
    def __init__(self, data):
        self.data = data
        self.regs = {}
    
    def coeffs(self, deg=1):
        ''' polynomial Coefficients '''
        if deg in self.regs:
            return self.regs[deg][0]
        ls = least_squares(self.data, deg=deg)
        self.regs[deg] = ls
        return ls[0]
    
    def error(self, deg=1):
        ''' R^2 error '''
        if deg in self.regs:
            return self.regs[deg][2]
        ls = least_squares(self.data, deg=deg)
        self.regs[deg] = ls
        return ls[2]
    
    def residual(self, deg=1):
        if deg in self.regs:
            return self.regs[deg][1]
        ls = least_squares(self.data, deg=deg)
        self.regs[deg] = ls
        return ls[1]
        
    def func(self, deg=1):
        ''' The regression polynomial as a function of x. '''
        y = self.coeffs(deg=deg)
        f = lambda x: sum([x**i * y[i] for i in xrange(len(y))])
        return f
        
