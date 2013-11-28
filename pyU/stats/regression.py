# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 19:59:09 2013

@author: David Edwards
"""
import random

from pyU.linalg.matrix import Matrix
from pyU.linalg.vectors import Vector


def lin_reg(data, return_err=False):
    """
    pass data as either [(x1,y1),..(xn,yn)] tuples or
    [[x_points], [y_points]]
    
    Uses Normal equation  xTxA = xTy to solve for the coefficients
    of the least squares line y = ax + b. Returns the vector (a, b)
    and optionally, the sum of the squared error. """
    if len(data) == 2:
        data = zip(data[0], data[1])
    
    y = Matrix([[d[1] for d in data]]).transpose()
    x = Matrix([[1, d[0]] for d in data])
    xTx = x.transpose() * x
    xTy = x.transpose() * y
    A = xTx.solve(xTy)
    if return_err:
        y_hat = x * Matrix(A._as_col)
        err = (y - y_hat).transpose() * (y - y_hat)        
        return A, err[0][0]
    return A
    

def least_squares(data, deg=1, return_err=False):
    """
    Uses Normal equation  xTxA = xTy to solve for the coefficients
    of least squares. Uses a polynomial of degree deg. 
    Optionally returns the sum of the squared error. 
    
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
    if return_err:
        y_hat = x * Matrix(A._as_col)
        err = (y - y_hat).transpose() * (y - y_hat)        
        return A, y_hat, y,err[0][0]
    return A
    

    
