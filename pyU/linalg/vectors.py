
from math import sqrt, acos, degrees, pi


class DimensionError(Exception):
    pass


class BaseVector(object):
    """
    Base class for vectors. Defines properties that 
    apply to vectors of n dimensions.
    
    """
    def __init__(self, vector):
        self.vector = list(vector)
        self.dim = len(self.vector)
        self._as_col = [[i] for i in self.vector]
    def __len__(self):
        return self.dim
        
    def __repr__(self):
        return str(self.vector)
    
    def __iter__(self):
        return iter(self.vector)
    
    def __add__(self, other):
        if not self.dim == other.dim:
            raise DimensionError
        v = [a+b for a,b in zip(self.vector, other.vector)]
        return type(self)(v)
    
    def __sub__(self, other):
        return self + other * -1
    
    def __mul__(self, scalar):
        if not type(scalar) in [int, float]:
            raise NotImplementedError
        v = [scalar * i for i in self.vector]
        return type(self)(v)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __eq__(self, other):
        try:
            return self.vector == other.vector
        except AttributeError:
            other = Vector(other)
            return self.vector == other.vector
    
    def __getitem__(self, item):
        return self.vector[item]
    
        
    def unit(self):
        mag = self.magnitude()
        v = [x / mag for x in self.vector]
        return type(self)(v)
    
    def magnitude(self):
        return sqrt(self.dot(self))
    
    def distance(self, other):
        d = self - other
        return d.magnitude()
    
    def angle_between(self, other, radians=False):
        dot_prod = self.dot(other)
        mag_prod = self.magnitude() * other.magnitude()
        theta = acos(dot_prod / mag_prod)
        if radians:
            return theta
        else:
            return degrees(theta)
            
    def proj_onto(self, other):
        scalar = self.dot(other) / other.dot(other)
        return other * scalar        
        
    def dot(self, other):
        if not self.dim == other.dim:
            raise DimensionError
        a, b = self.vector, other.vector
        return sum(x*y for x,y in zip(a, b))


class Vector(BaseVector):
    
    """ 
    2 or 3 Dimensional Euclidian Vector 
    
    """
    def __init__(self, vector):
        BaseVector.__init__(self, vector)
    
    def cross(self, other):
        """
        cross product of two 3-D vectors.
        
        """
        if not self.dim + other.dim == 6:
            raise DimensionError
        a, b = self, other
        x, y, z = 0, 1, 2
        vx = a[y]*b[z] - a[z]*b[y]
        vy = a[z]*b[x] - a[x]*b[z]
        vz = a[x]*b[y] - a[y]*b[x]
        return Vector([vx, vy, vz])
    
    def triple_scalar_prod(self, v1, v2):
        v3 = v1.cross(v2)
        return self.dot(v3)
    
    def coord_angles(self, radians=False):
        """
        3-D vector method that
        returns the coordinate angle from 
        each positive axis in the form
        [angle from x, angle from y, angle from z] 
        
        """
        if not self.dim == 3:
            raise DimensionError
        u = self.unit()
        if radians:
            angles = [acos(i) for i in u]
        else:
            angles = [degrees(acos(i)) for i in u]
            
        return angles
        
    def polar_angle(self, radians=False):
        """ 
        Returns counter-clockwise angle from 
        the positive x-axis of a 2-d vector. 
        
        """
        if not self.dim == 2:
            raise DimensionError
        ux = Vector([1, 0])
        theta = self.angle_between(ux, radians=True)
        if self[1] < 0:
            theta = 2*pi - theta
        if radians:
            return theta
        return degrees(theta) 

