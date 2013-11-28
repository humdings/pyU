# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 23:26:06 2013

@author: edwards7011
"""

from matrix import Matrix
from vectors import Vector

def gram_schmidt(S, normal=True):
    """
    Gram Schmidt ortho/orthonormalize a set of vectors
    """
    s = [S[0]]
    for i in xrange(1, len(S)):
        ui = S[i]
        for j in xrange(i):
            ui -= ui.proj_onto(s[j])
        s.append(ui)
    if normal:
        return [i*(1./i.magnitude()) for i in s]
    return s
    
    
    
    
    
    
    
