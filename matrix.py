# Author: Jef Wagner
# Date: 10-02-2015

import numpy as np
import numbers

from vec import *

class GenMat:
	"""General matrices, base class for square matrices and affine matrices"""

	def __init__(self, nrows, ncolumns, *args):
		"""
		Constructor of the GenMat class
			usage: GenMat( 2,3, [1,2,3,4,5,6])
				- first two arguments are the size
				- following argument(s) is(arg) the data
		"""
		A = np.array( args, dtype=np.float32)
		n = len(A.flatten())
		if n == nrows*ncolumns:
			self.array = A.reshape(nrows,ncolumns)
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.__init__ takes and array with {} elements".format(name, nrows*ncolumns))

	def __len__(self):
		"""Number of rows in the matrix"""
		return( len(self.array))

	def __getitem__(self, index):
		"""Defines the `[]` operator"""
		return( self.array[index])

	def __iter__(self):
		"""Defines the iterator for the matrix"""
		return( iter(self.array))

	def __repr__(self):
		"""Defines how the class is printed or shown in the command line"""
		name = self.__class__.__name__
		newline = ",\n"+(" "*(len(name)+2))
		nrows,ncolumns = self.array.shape
		fmtstr = name+"(["+(newline.join(["{}"]*nrows))+"])"
		rows = [[x for x in row] for row in self.array]
		return( fmtstr.format(*rows))

	def __mul__(self, other):
		"""Defined multiplication as the dot product"""
		return( self.dot(other))

class SquareMat(GenMat):
	"""General square matrices"""

	def __init__(self, n, *args):
		super(SquareMat, self).__init__(n,n,*args)

	def dot(self, other):
		"""Define the dot product for vectors and other matrices"""
		n = len(self)
		if isinstance(other, FloatVec) and len(self) == n:
			new_v = np.dot( self.array, other.array.reshape(n,1))
			return( other.__class__(new_v))
		elif isinstance(other, self.__class__):
			new_m = np.dot( self.array, other.array)
			return( self.__class__(new_m))
		else:
			raise AttributeError("obadoba")

	def inv(self):
		"""Define the inverse of the matrix"""
		Ainv = np.linalg.inv(self.array)
		return( self.__class__(Ainv))

class Mat2x2(SquareMat):
	"""A 2x2 matrix"""

	def __init__(self, *args):
		super(Mat2x2, self).__init__(2, *args)

class Mat3x3(SquareMat):
	"""A 3x3 matrix"""

	def __init__(self, *args):
		super(Mat3x3, self).__init__(3, *args)

class Mat4x4(SquareMat):
	"""A 4x4 matrix"""

	def __init__(self, *args):
		super(Mat4x4, self).__init__(4, *args)

class AffineMat(GenMat):
	"""Matrics to represent affine transforms on vectors"""

	def __init__(self, n, *args):
		super(AffineMat, self).__init__(n,n+1,*args)

	def dot(self, other):
		"""Define the dot product for vectors and other matrices"""
		n = len(self)
		if isinstance(other, FloatVec) and len(self) == n:
			v = np.append( other.array, 1.)
			new_v = np.dot( self.array, v.reshape(n+1,1))
			return( other.__class__(new_v))
		elif isinstance(other, self.__class__):
			bv = [0]*n+[1]
			ml = np.append( self.array, bv, axis = 0)
			mr = np.append( other.array, bv, axis = 0)
			new_m = np.dot( ml, mr).resize((n,n+1))
			return( self.__class__(new_m))
		else:
			raise AttributeError("boo")

	def inv(self):
		"""Define the inverse of the affine transform"""
		n = len(self.array)
		A = self.array[:,0:n]
		b = self.array[:,n]
		Ainv = np.linalg.inv(A)
		binv = -np.dot( Ainv, b.reshape(1,n)).flatten()
		new_m = np.append( Ainv, binv, axis=1)
		return( self.__class__(new_m))

class Mat2x3(AffineMat):
	"""A 2x3 matrix for Vec2 objects"""

	def __init__(self, *args):
		super(Mat2x3, self).__init__(2, *args)

	def to_square(self):
		n = len(self)
		bv = [0]*n+[1]
		new_m = np.append( self.array, bv, axis = 0)
		return( Mat3x3( new_m))

class Mat3x4(AffineMat):
	"""A 3x4 matrix for Vec3 objects"""

	def __init__(self, *args):
		super(Mat3x4, self).__init__(3, *args)

	def to_square(self):
		n = len(self)
		bv = [0]*n+[1]
		new_m = np.append( self.array, bv, axis = 0)
		return( Mat4x4( new_m))
