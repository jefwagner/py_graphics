# Author: Jef Wagner
# Date: 10-02-2015

import numpy as np
import numbers

from vector import BaseVec, FloatVec

__all__ = ['Mat2x2','Mat3x3','Mat4x4','Mat2x3','Mat3x4']

###############################################################
# GenMat class
# ============
# This class is the base class for matrices. It implements:
# - formatted printing (__repr__)
# - equality (__eq__)
# - almost equality (close)
# - behavior of the `*` operator (__mul__)
class GenMat(BaseVec):
	"""General matrix base class for SquareMat and AffineMat"""

	# __init__ method
	# ---------------
	# It calls the BaseVec's constructor, then reshapes the array to
	# a two-dimensional array.
	def __init__(self, nrows, ncolumns, *args):
		"""Constructor of the GenMat class"""
		super(GenMat, self).__init__(np.float32, nrows*ncolumns, *args)
		self.array = self.array.reshape(nrows, ncolumns)

	# __repr__ method
	# ---------------
	# This method defines how the object is displayed when either
	# the `print` command or the `format` method is called, or how it
	# is displayed in the command line.
	#
	# Example:
	# >>> m = Mat3x3(range(9))
	# >>> m
	# Mat3x3([[0.0, 1.0, 2.0],
    # 		  [3.0, 4.0, 5.0],
    # 		  [6.0, 7.0, 8.0]])
	def __repr__(self):
		"""Defines how the class is printed or shown in the command line"""
		name = self.__class__.__name__
		newline = ",\n"+(" "*(len(name)+2))
		nrows,ncolumns = self.array.shape
		fmtstr = name+"(["+(newline.join(["{}"]*nrows))+"])"
		rows = [[x for x in row] for row in self.array]
		return( fmtstr.format(*rows))

	# __eq__ method
	# -------------
	# Defined the behavior for the `==` comparison operator. Performs
	# element by element comparison. Raises and exceptions if the
	# the objects are of different size.
	#
	# Example:
	# >>> m = Mat2x2(1,0,0,1)
	# >>> m == [[1,0],[0,1]]
	# True
	def __eq__(self, other):
		"""Equality comparison operator"""
		oarray = np.array(other)
		if self.array.shape == oarray.shape:
			test_array = [x==y for x,y in zip(self.array.flatten(), oarray.flatten())]
			return( all(test_array))
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.__eq__ takes an {} array".format(name, self.array.shape))

	# close method
	# ------------
	# Define a test for almost equal.
	# This works by casting the other argument as a numpy array
	# and using numpy's `allclose` function.
	#
	# Example:
	# >>> m = Mat2x2(1,0,0,1)
	# >>> almost_m = Mat2x2(1-1.e-10,1.e-10,0,1)
	# >>> m == almost_m
	# False
	# >>> m.close([1-1.e-10,0],[1.e-10,1])
	# True
	def close(self, other, rtol = 1.e-5, atol = 1.e-8):
		"""Comparison within some tolerance"""
		oarray = np.array(other)
		if self.array.shape == oarray.shape:
			return( np.allclose(self.array, oarray, rtol, atol))
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.close takes an {} array".format(name, self.array.shape))

	# __mul__ method
	# --------------
	# overrides the `*` operator to call the dot product either
	# matrix-vector, or matrix-matrix.
	# 
	# Example:
	# >>> m = Mat2x2(0,1,1,0)
	# >>> v = Vec2(1,0)
	# >>> m*v
	# Vec2([ 0.0, 1.0])
	# >>> m*m
	# Mat2x2([[ 1.0, 0.0],
	#	      [ 0.0, 1.0])
	def __mul__(self, other):
		"""Multiplication as the dot product"""
		return( self.dot(other))


################################################################
# SquareMat class
# ===============
# A base class for square matrices. It provides
# - Defines the dot product (dot)
# - Defines the inverse (inv)
class SquareMat(GenMat):
	"""Square matrix base class for Mat2x2, Mat3x3, and Mat4x4"""

	# __init__ method
	# ---------------
	# Simply calls the GenMat constructor with two equal arguments
	def __init__(self, n, *args):
		"""Constructor of the SquareMat class"""
		super(SquareMat, self).__init__(n,n,*args)

	# dot method
	# ----------
	# Calculates matrix-vector and matrix-matrix dot product
	# uses numpy's dot product, raises an exception for anything
	# else.
	#
	# Example:
	# >>> m = Mat2x2(0,1,1,0)
	# >>> v = Vec2(1,0)
	# >>> m.dot(v)
	# Vec2([ 0.0, 1.0])
	# >>> m.dot(m)
	# Mat2x2([[ 1.0, 0.0],
	#	      [ 0.0, 1.0])
	def dot(self, other):
		"""Dot product for matrix-matrix and matrix-vector"""
		n = len(self)
		if isinstance(other, FloatVec) and len(self) == n:
			new_v = np.dot( self.array, other.array.reshape(n,1))
			return( other.__class__(new_v))
		elif isinstance(other, self.__class__):
			new_m = np.dot( self.array, other.array)
			return( self.__class__(new_m))
		else:
			raise AttributeError("obadoba")

	# inv method
	# ----------
	# Calculates the inverse of the matrix using numpy's linear
	# algebra module. Checks to see if the matrix is singular.
	# 
	# Example:
	# >>> m = Mat2x2(0,1,1,0)
	# >>> m.inv()
	# Mat2x2([[0.0, 1.0],
	#         [1.0, 0.0]])
	def inv(self):
		"""Inverse of the matrix"""
		if np.fabs(np.linalg.det(self.array)) > 1.e-10:
			Ainv = np.linalg.inv(self.array)
			return( self.__class__(Ainv))
		else:
			raise ValueError("Can not take inverse of singular matrix")


##################################################################
# Mat2x2 class
# ============
# A 2x2 matrix, does not add any functionality
class Mat2x2(SquareMat):
	"""A 2x2 matrix"""

	# __init__ method
	# ---------------
	#
	# Example:
	# >>> m22 = Mat2x2(1,0,0,1)
	def __init__(self, *args):
		"""Constructor of the Mat2x2 class"""
		super(Mat2x2, self).__init__(2, *args)

##################################################################
# Mat3x3 class
# ============
# A 3x3 matrix, does not add any functionality
class Mat3x3(SquareMat):
	"""A 3x3 matrix"""

	# __init__ method
	# ---------------
	#
	# Example:
	# >>> m33 = Mat3x3([0,0,1],[0,1,0],[1,0,0])
	def __init__(self, *args):
		"""Constructor of the Mat3x3 class"""
		super(Mat3x3, self).__init__(3, *args)

##################################################################
# Mat4x4 class
# ============
# A 4x4 matrix, does not add any functionality
class Mat4x4(SquareMat):
	"""A 4x4 matrix"""

	# __init__ method
	# ---------------
	#
	# Example:
	# >>> m44 = Mat4x4(range(16))
	def __init__(self, *args):
		"""Constructor of the Mat4x4 class"""
		super(Mat4x4, self).__init__(4, *args)

###############################################################
# AffineMat class
# ===============
# A base class that define affine transformations on vectors.
# This base class provides:
# - a dot product (dot)
# - an inverse (inv)
# - a method to turn the matrix into a square matrix
class AffineMat(GenMat):
	"""Affine matrix base class for Mat2x3 and Mat3x4"""

	# __init__ method
	# ---------------
	# Calls the parents init with n, and n+1
	def __init__(self, n, *args):
		"""Constructor of the AffineMat class"""
		super(AffineMat, self).__init__(n,n+1,*args)

	# dot method
	# ----------
	# Affine transformation can be though as a combination of a matrix
	# transformation and a displacement. This simply defines how an affine
	# transformation is applied to a vector, or how multiple transformations
	# are combined.
	def dot(self, other):
		"""Dot product for matrix-matrix and matrix-vector"""
		n = len(self)
		if isinstance(other, FloatVec) and len(self) == n:
			v = np.append( other.array, 1.)
			new_v = np.dot( self.array, v.reshape(n+1,1))
			return( other.__class__(new_v))
		elif isinstance(other, self.__class__):
			bv = [0]*n+[1]
			ml = np.append( self.array, [bv], axis=0)
			mr = np.append( other.array, [bv], axis=0)
			new_m = np.resize(np.dot( ml, mr),(n,n+1))
			return( self.__class__(new_m))
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.dot take with an AffineMat or FloatVec".format(name))

	# inv method
	# ----------
	# Finds the inverse affine transformation.
	def inv(self):
		"""Inverse of the affine transform"""
		n = len(self.array)
		A = self.array[:,0:n]
		b = self.array[:,n]
		if np.fabs(np.linalg.det(A)) > 1.e-10:
			Ainv = np.linalg.inv(A)
			binv = -np.dot( Ainv, b.reshape(n,1))
			new_m = np.append( Ainv, binv, axis=1)
			return( self.__class__(new_m))
		else: 
			raise ValueError("Can not take inverse of singular matrix")


##################################################################
# Mat2x3 class
# ============
# A 2x3 matrix, provies:
# - a method for providing a square matrix (to_square)
class Mat2x3(AffineMat):
	"""A 2x3 matrix for Vec2 objects"""

	# __init__ method
	# ---------------
	#
	# Example:
	# >>> m23 = Mat2x3([1,2,3,4,5,6])
	def __init__(self, *args):
		"""Constructor of the Mat2x3 class"""
		super(Mat2x3, self).__init__(2, *args)

	# to_square method
	# ----------------
	# Returns a Mat3x3 with [0,0,1] in the bottom row
	def to_square(self):
		"""Returns a Mat3x3 with [0,0,1] in the bottom row"""
		bv = [0,0,1]
		new_m = np.append( self.array, [bv], axis=0)
		return( Mat3x3( new_m))

##################################################################
# Mat3x4 class
# ============
# A 3x4 matrix, provies:
# - a method for providing a square matrix (to_square)
class Mat3x4(AffineMat):
	"""A 3x4 matrix for Vec3 objects"""

	# __init__ method
	# ---------------
	#
	# Example:
	# >>> m34 = Mat3x4([1]*12)
	def __init__(self, *args):
		"""Constructor of the Mat3x4 class"""
		super(Mat3x4, self).__init__(3, *args)

	# to_square method
	# ----------------
	# Returns a Mat4x4 with [0,0,0,1] in the bottom row
	def to_square(self):
		"""Returns a Mat4x4 with [0,0,0,1] in the bottom row"""
		bv = [0,0,0,1]
		new_m = np.append( self.array, [bv], axis=0)
		return( Mat4x4( new_m))
