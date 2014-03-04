# -*- coding: utf-8 -*-
import numpy as np
import random
from pyU.linalg.matrix import *
import unittest
from pyU.utils import sig_figs



epsilon = 1.0e-9
dec_places = 9


n = random.randint(2,50)
b = [random.randint(-100,100) for _ in xrange(n)]
np_matA = np.array(randMatrix(n, n).rows)
np_matB = np.array(randMatrix(n, n).rows)
np_matC = np.array(randMatrix(n, n).rows)

matA = Matrix(np_matA)
matB = Matrix(np_matB)
matC = Matrix(np_matC)

_I = I(n)
_Zero = Zero(n)

print
print "=============================================="
print
print "Test conducted using %s x %s Matrices"%(n,n)
print
print "=============================================="
print

class MatrixTest(unittest.TestCase):
    
    def test_solve(self, epsilon=epsilon):
        np_ans = np.linalg.solve(np_matA, b)
        matans = matA.solve(b)
        for i in xrange(n):
            self.assertAlmostEqual(
                np_ans[i] ,matans[i], places=dec_places
            )
    def test_det(self, sigs=10):
        """ 
        Test if the determinant is within sigs 
        sig figs of numpy det. 
        """
        np_ans = sig_figs(np.linalg.det(np_matA), sig=sigs)
        matans = sig_figs(matA.det(), sig=sigs)
        self.assertEqual(matans, np_ans)
    
    def test_add(self, epsilon=epsilon):
        np_ans = np_matA + np_matB
        matans = matA + matB
        for i in xrange(n):
            for j in xrange(n):
                self.assertAlmostEqual(
                    np_ans[i][j], matans[i][j], places=dec_places
                )

    def test_multiplication(self):
        np_ans = np_matA.dot(np_matB)
        matans = matA * matB
        for i in xrange(n):
            for j in xrange(n):
                self.assertAlmostEqual(
                    np_ans[i][j], matans[i][j], places=dec_places
                )
    
    def test_properties(self):
        # multiplication
        # Associative property
        try:
            self.assertEqual(matA*(matB*matC), (matA*matB)*matC)
        except AssertionError:
            print "Resorted to soft equals at associative mult"
            M, N = matA*(matB*matC), (matA*matB)*matC
            self.assertTrue(M._soft_eq(N))            
        # Distributive property
        try:
            self.assertEqual(matA*(matB + matC), matA*matB + matA*matC)
        except AssertionError:
            print "Resorted to soft equals at distrib mult 1"
            M, N = matA*(matB + matC), matA*matB + matA*matC
            self.assertTrue(M._soft_eq(N))   
        try:
            self.assertEqual((matA + matB)*matC, matA*matC + matB*matC)
        except AssertionError:
            print "Resorted to soft equals at distrib mult 2"
            M, N = (matA + matB)*matC, matA*matC + matB*matC
            self.assertTrue(M._soft_eq(N)) 
        # Mult Identity
        self.assertEqual(_I*matA, matA)
        self.assertEqual(matB*_I, matB)
        # Addition
        # Commutative
        try:
            self.assertEqual(matA + matB, matB + matA)
        except AssertionError:
            print "Resorted to soft equals commutative addition"
            M, N = matA + matB, matB + matA
            self.assertTrue(M._soft_eq(N))
        # Associative
        try:
            self.assertEqual(matA + (matB + matC), (matA + matB) + matC)
        except AssertionError:
            print "Resorted to soft equals associative addition"
            M, N = matA + (matB + matC), (matA + matB) + matC
            self.assertTrue(M._soft_eq(N))
        # Additive inverse
        self.assertEqual(matA - matA, _Zero)
        

if __name__ == '__main__':
    unittest.main()
        


        
        
