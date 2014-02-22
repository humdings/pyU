from __future__ import division
import random
from vectors import Vector


class DimensionError(Exception):
    pass


class Matrix(object):
    
    """A list containg the row vectors of a Matrix"""
    
    def __init__(self, vectors):
        self.rows = [Vector(i) for i in vectors]
        self._validate()
        self.columns = [
            Vector(x) for x in zip(*self.rows)
        ]
        self.nrows = len(self.rows)
        self.ncols = len(self.columns)
        self.size = (self.nrows, self.ncols)
        self.is_square = self.nrows == self.ncols
        self.PLU = None
    
    #######################
    #  Operator overloads #
    #######################
    
    def __add__(self, B):
        if not type(B) == Matrix:
            B = Matrix(B)
        if not self.size == B.size:
            raise DimensionError()
        rows = [self[i] + B[i] for i in xrange(self.nrows)]
        return Matrix(rows)
    
    def __sub__(self, B):
        if not type(B) == Matrix:
            B = Matrix(B)
        B = B._scale_by(-1)
        return self + B
        
    def __getitem__(self, item):
        return self.rows[item]
        
    def __eq__(self, B):
        """
        Uses the definition of Matrix equality:
            1. Matrices must be the same size.
            2. A(i,j) = B(i,j) for every component (i,j)
        
        Relys on list equality to compare entire rows at once.
        """
        if not type(B) == Matrix:
            B = Matrix(B)
        if not self.size == B.size:
            return False
        for i in range(self.nrows):
            if not self[i] == B[i]:
                return False
        return True
    
    def __repr__(self):
        s = ""
        for row in self.rows:
            s += str(row) + "\n"
        return s  
    
    def __mul__(self, B):
        try:
            return self._times(B)
        except TypeError, DimensionError:
            return self._scale_by(B)
    
    def __rmul__(self, scalar):
        return self * scalar
    
    def __pow__(self, n):
        if not type(n) == int or n < 0:
            raise NotImplementedError(
                'Only integers >= 0 are supported'
                )
        M = self
        if n == 0:
            return I(self.nrows)
        for _ in range(1,n):
            M = M * self
        return Matrix(M)
        
    #################
    # Local Methods #
    #################
    
    def _soft_eq(self, B, round_to=7):
        # local method to adjust for rounding error
        if not self == B:
            return True
        for i in range(self.nrows):
            for j in range(self.ncols):
                if not round(self[i][j], round_to) == round(B[i][j], round_to):
                    return False
        return True
    
    def _times(self, B):
        if not type(B) == Matrix:
            B = Matrix(B)
        if not self.ncols == B.nrows:
            raise DimensionError()
        rows = [[dot(row, col) for col in B.columns] for row in self]
        return Matrix(rows)
    
    def _scale_by(self, scalar):
        R = []
        for i in range(self.nrows):
            R.append(self._scale_row(i, scalar))
        return Matrix(R)
    
    def _scale_row(self, row, scalar):
        """ 
        Local method for scaling rows. 
        Returns a scaled row as a list. 
        
        """
        r = self[row]
        return map(lambda x: x * scalar, r)
    
    def _validate(self):
        s = set(len(row) for row in self.rows)
        if not len(s) == 1:
            raise DimensionError()
        
    def comp(self, i, j):
        """ NOTE: indexing starts at zero"""
        return self[i][j]
    
    def transpose(self):
        return Matrix(self.columns)

    #############################
    # Elementary Row Operations #
    #############################

    def permute(self, i, j):
        """ 
        Swap rows i & j 
        
        """
        new_rows = self.rows
        row_i = new_rows[i]
        new_rows[i] = new_rows[j]
        new_rows[j] = row_i
        return Matrix(new_rows)
    
    def scale_row(self, row, scalar):
        """ 
        row_i ===> c*row_i 
        
        """
        r = self.rows
        r[row] = self._scale_row(row, scalar)
        return Matrix(r)
    
    def add_row_multiple(self, i, j, scalar=1):
        """ 
        row_i ===> row_i + c*row_j 
        
        """
        rows = self.rows
        row_i = self.rows[i]
        row_j = self._scale_row(j, scalar)  # c*row_j
        rows[i] = map(lambda x, y: x + y, row_i, row_j)
        return Matrix(rows)
        
    def det(self):
        if not self.is_square:
            raise DimensionError
        n = self.nrows
        PLU = self.lu_decomp()
        a = (-1)**PLU[0].n_perms
        b = 1
        for i in xrange(n):
            b *= PLU[1][i][i]
            b *= PLU[2][i][i]
        return a * b
            
    
    def lu_decomp(self):
        """
        returns (P, L, U) such that P*self = L*U.
        """
        if not self.is_square:
            raise DimensionError
        n = self.nrows
        L = [[0.]*n for i in xrange(n)]
        U = [[0.]*n for i in xrange(n)]
        P = PermutationMatrix(self)
        M = P * self
        for j in xrange(n):
            L[j][j] = 1.
            for i in xrange(j + 1):
                s1 = sum(U[k][j] * L[i][k] for k in xrange(i))
                U[i][j] = M[i][j] - s1
            for i in xrange(j, n):
                s2 = sum(U[k][j] * L[i][k] for k in xrange(j))
                L[i][j] = (M[i][j] - s2) / U[j][j]
        self.PLU = (P, Matrix(L), Matrix(U))
        return self.PLU
            
    def solve(self, b):
        """ solve Ax = b using LU factorization of A. """
        if type(b) == Matrix:
            if not b.ncols == 1:
                raise DimensionError("b must be a  1-d list, Vector or n x 1 matrix")
        elif type(b) == Vector:            
            b = Matrix(b._as_col)
        else:
            b = Matrix(Vector(b)._as_col)
            #b = Matrix([Vector(b)]).transpose()      # make sure b is a vector
        # else:
        #     b = Matrix([b]).transpose()
        if self.PLU is not None:
            PLU = self.PLU
        else:
            PLU = self.lu_decomp()
        P, L, U = PLU
        n = self.nrows        
        # Need to solve Ly = b for y, where y = Ux 
        b = Vector(zip(*(P * b))[0])
        
        #for i in xrange(n):
        #    if P[i][i] == 0 or L[i][i] == 0:
        #        raise ValueError("there was a zero along a diagonal")
        y_0 = b[0] / L[0][0] 
        y = [y_0]
        for i in xrange(1,n):
            y_i = (
                b[i] - sum([L[i][j] * y[j] for j in xrange(i)] )
            )
            y.append(y_i / float(L[i][i]))
        
        x_n = y[n-1] / U[n-1][n-1]
        x = {n-1: x_n}
        for i in xrange(n-1, -1, -1):
            x_i = (
                y[i] - sum([U[i][j] * x[j] for j in xrange(i+1, n)])
            )
            x[i] = x_i / float(U[i][i])
        x = Vector([x[i] for i in x])
        return x


class I(Matrix):
    def __init__(self, n):
        basis = [
            [float(i == j) for i in xrange(n)] for j in xrange(n)
        ]        
        super(I, self).__init__(basis)


class Zero(Matrix):
    def __init__(self, n):
        Z = [[0.]*n]*n 
        super(Zero, self).__init__(Z)


class PermutationMatrix(Matrix):
    """ A permutation matrix for the input matrix. """
    def __init__(self, aMatrix):
        self.n_perms = 0
        M = aMatrix
        if not type(M) == Matrix:
            M = Matrix(M)
        if not M.is_square:
            raise DimensionError
        n = M.nrows
        _I = I(n)
        for j in xrange(n):
            row = max(xrange(j, n), key=lambda i: M[i][j])
            if not j == row:
                _I.permute(j, row)
                self.n_perms += 1
        super(PermutationMatrix, self).__init__(_I.rows)

