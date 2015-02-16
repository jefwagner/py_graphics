# Author: Jef Wagner
# Date: 10-02-2015

import numpy as np
import numbers

__all__ = ['Vec2', 'Vec3', 'Vec4', 
					 'IVec2', 'IVec3', 'IVec4']

#####################################################################
# BaseVec
# ======
# This is the base class for general vector objects.
#
# It is mostly a wrapper for a fixed sized numpy.array, so most of 
# the functionality is based off of the numpy.array class.
# 
# It implements
# + A constructor (__init__)
# + The `len` command (__len__)
# + The `[]` operator (__getitem__)
# + Iteration (__iter__)
# + Formatted printing (__repr__)
class BaseVec:
	"""Base class for vector object, provides sequence functionality"""

	# BaseVec constructor
	# ------------------
	# This constructor takes 2+ positional arguments
	# - type: a numpy dtype as the data type of the vector
	# - n: an integer as the size of the vector
	# - *args: the values for the vector
	def __init__(self, type, n, *args):
		"""Constructor for the GenVec class."""
		array = np.array( args, dtype=type).flatten()
		if len(array) == n:
			self.array = array
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.__init__ takes an array of length {}".format(self.name, n))

	# __len__ method
	# --------------
	# Defines the behavior when the built-in `len` function. Simply 
	# passes numpy array to the `len` object.
	# 
	# Example:
	# >>> v = Vec2(0,1)
	# >>> len(v)
	# 2
	def __len__(self):
		"""Length of the vector"""
		return( len(self.array))

	# __getitem__ method
	# ------------------
	# Defines the behavior for the `[]` operator. Simply applies the
	# same `[]` to the numpy array. That way all the slice operations
	# will work.
	#
	# Example: Shows getting an element, and a slice 
	# >>> v = IVec4(1,2,3,4)
	# >>> v[0]
	# 1
	# >>> v[1:2]
	# np.array([2,3])
	def __getitem__(self, index):
		"""Retrieve the (index)th item of the vector"""
		return( self.array[index])

	# __iter__ method
	# ---------------
	# Defines how the object workds in loops. Simply uses the iterator
	# of the numpy array.
	#
	# Example:
	# >>> v = IVec4(2,1,4,3)
	# >>> for x in v:
	# ...     print( x)
	# ...
	# 2
	# 1
	# 4
	# 3
	def __iter__(self):
		"""Returns an iterator for the matrix"""
		return( iter(self.array))

	# __repr__ method
	# ---------------
	# Defines a formatted printing method for the format command and
	# the from the command line interface.
	#
	# Example:
	# >>> v = IVec2(1,1)
  # >>> v
  # IVec2([ 1, 2])
	def __repr__(self):
		"""Defines how the class is printed or shown in the command line"""
		name = self.__class__.__name__
		return "{}({})".format(name,[x for x in self])


#####################################################################
# GenVec
# ======
# This is the base class for algebraic vector objects.
#
# It defines the arithmetic for general vectors
# 
# It implements
# + The comparison `==` operator (__eq__)
# + An almost equal comparison function (close)
# + The unary `-` operator (__neg__)
# + The bianary `+` operator (__add__ and __radd__)
# + The bianary `-` operator (__sub__ and __rsub__)
# + The bianary `*` operator (__mul__ and __rmul__)
# + The bianary `/` operator (__truediv__)
class GenVec(BaseVec):
	"""General vector object, only used as a base class for FloatVec and IntVec"""

	# __eq__ method
	# -------------
	# Defines the equality comparison operator. Comparison runs over
	# all elements, and returns true if all return true.
	def __eq__(self, other):
		"""Equality comparison operator"""
		if len(other) == len(self):
			return( all( [x==y for x, y in zip(self,other)]))
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.__eq__ takes a sequence of length {}".format(name, len(self)))

	# close method
	# ------------
	def close(self, other, rtol=1.e-5, atol=1.e-8):
		"""Comparison within some tolerance"""
		oarray = np.array(other).flatten
		if len(oarray) == len(self):
			return( np.allclose( self.array, oarray, rtol, atol))
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.close takes a sequence of length {}".format(name, len(self)))

	# __neg__ method
	# --------------
	# Defines unary `-` operator. Performs a elementwise negation using
	# a list comprehension then cast the result as a new object.
	#
	# Example:
	# >>> v = IVec2(1,2)
	# >>> -v
	# IVec2([ -1, -2])
	def __neg__(self):
		"""Negative of all elements of the vector"""
		return( self.__class__([-x for x in self]))

	# __add__ and __radd__ methods
	# ----------------------------
	# Defines the bianary `+` operator. Both scalar addition, which adds
	# the same number to each element and vector addition, which adds
	# elementwise.
	#
	# Example:
	#	>>> A = Vec2(0,1)
	#	>>> B = A+1; B
	#	Vec2([1.0,2.0])
	#	>>> C = b+[1,-1]; C
	#	Vec2([2.0,1.0])
	def __add__(self, other):
		"""Defines the `+` operator for scalars and sequence types""" 
		if isinstance( other, numbers.Number):
			return( self.__class__([x+other for x in self]))
		else:
			array = np.array( other, dtype=self.array.dtype).flatten()
			if len(array) == len(self):
				return( self.__class__([x+y for x,y in zip(self,array)]))
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__add__ takes a scalar or an array with {} elements".format(name, len(self)))

	# Same operator for right addition.
	__radd__ = __add__

	# __sub__ and __rsub__ methods
	# --------------------------
	# Defines the bianary `-` operator. Both scalar and vector
	# subtraction.
	def __sub__(self, other):
		"""Defines the `-` operator for scalars and sequence types """
		if isinstance( other, numbers.Number):
			return( self.__class__([x-other for x in self]))
		else:
			array = np.array( other, dtype=self.array.dtype).flatten()
			if len(array) == len(self):
				return( self.__class__([x-y for x,y in zip(self,array)]))
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__sub__ takes a scalar or an array with {} elements".format(name, len(self)))

	# Same stuff, but for right subtraction this time.
	def __rsub__(self, other):
		"""Defines the `-` operator for scalars and sequence types"""
		if isinstance( other, numbers.Number):
			return( self.__class__([other-x for x in self]))
		else:
			array = np.array( other, dtype=self.array.dtype).flatten()
			if len(array) == len(self):
				return( self.__class__([y-x for x,y in zip(self,array)]))
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__sub__ takes a scalar or an array with {} elements".format(name, len(self)))

	# __mul__ and __rmul__ methods
	# ----------------------------
	# Defines the bianary `*` operator. Scalar multiplication only
	def __mul__(self, other):
		"""Defines the `*` operator for scalars """
		if isinstance( other, number.Number):
			return( self.__class__([x*other for x in self]))
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.__mul__ takes a scalar".format(name))

  # Same exact operator for right multiplication
	__rmul__ = __mul__

	# __truediv__ method
	# ------------------
	# Defines the bianary `/` operator. left scalar division only
	def __truediv__(self, other):
		"""
		Defines the `/` operator for scalars 
		"""
		if isinstance(other, numbers.Number):
			return( self.__class__([x/other for x in self]))
		else:
			raise AttributeError("{}.__truediv__ takes a scalar".format(name))


######################################################################
# FloatVec
# ========
# This is the base class for vectors with floating point elements.
# 
# It implements
# + inner product (inner)
# + overloads the bianary `*` (__mul__ and __rmul__)
# + magnitude of the vector (mag) 
# + normalized vector (unit)
class FloatVec(GenVec):
	"""A vector of floats, a base class for Vec2, Vec3, and Vec4"""

	# FloatVec constructor
	# --------------------
	# Simply passes the initialization to the parent classes constructor
	def __init__(self, n, *args):
		"""Constructor for the FloatVec method"""
		super(FloatVec,self).__init__(np.float32, n, *args)

	# inner method
	# ------------
	# Inner produt between two vectors. The argument of the method can
	# be any sequence type of the same length. If the second sequence
	# is a different length it raises an exception.
	#
	# Example:
	# >>> v = Vec3([2,0,1])
	# >>> v.inner([-1,0,1])
	# -1.0
	def inner(self, other):
		"""Defines the inner product for two equal length sequences"""
		if len(self) == len(other):
			return( sum([x*float(y) for x, y in zip(self,other)]))
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.inner takes a length {} sequence".format(name,len(self)))

	# __mul__ method
	# --------------
	# Defines the `*` operator. Does type checking, if it is a scalar
	# object it performs scalar multiplication, otherwise it performs
	# the inner product.
	def __mul__(self, other): 
		"""
		Overloads the `*` operator to either give scalar multiplication, 
		or the inner product
		""" 
		if isinstance(other, numbers.Number): 
			return( self.__class__([x*other for x in self])) 
		else: 
			return( self.inner(other))

	# Same exact operator for right multiplication
	__rmul__ = __mul__

	# mag method
	# ----------
	# Finds the magnitude of a vector, defined as the square root of the
	# inner product of the vector with itself.
	def mag(self):
		"""Defines the magnitude of a vector"""
		return( np.sqrt(self.inner(self)))

	# unit method
	# -----------
	# Finds the unit vector, divides the vector by the magnitude. If the
	# maginitude of the vector is 0, then it raises and exception.
	#
	# Example:
	# >>> v = Vec2( 3, 4)
	# >>> v.unit()
	# Vec2([ 0.6, 0.8])
	def unit(self):
		"""Defines the unit vector in the same direction"""	
		l = self.mag()
		if l != 0:
			return( self/l)
		else:
			name = self.__class__.__name__
			raise ValueError("{}.unit does not work for the 0 vector".format(name))


######################################################################
# Vec2
# ====
# A 2-component vector of floats.
# 
# It implements
# + cross product (cross)
class Vec2(FloatVec):
	"""A two component vector"""

	# Vec2 constructor
	# ----------------
	def __init__(self, *args):
		super(Vec2, self).__init__(2, *args)

	# cross method
	# ------------
	# Find the cross product with two 2-component vectors and returns
	# a scalar
	def cross(self, other):
		"""Defines the 2-d cross product, returns a scalar"""
		if len(other) == 2:
			return( self[0]*other[1]-self[1]*other[0])
		else:
			raise AttributeError("Vec2.cross takes a length 2 sequence")

######################################################################
# Vec3
# ====
# A 3-component vector of floats.
# 
# It implements
# + cross product (cross)
class Vec3(FloatVec):
	"""A three component vector"""

	# Vec3 constructor
	# ----------------
	def __init__(self, *args):
		super(Vec3, self).__init__( 3, *args)

	# cross method
	# ------------
	# Find the cross product with two 3-component vectors and returns
	# a new Vec3 object.
	def cross(self, other):
		"""Defines the 3-d cross product, returns another Vec3"""
		if len(other) == 3:
			x = self[1]*other[2]-self[2]*other[1]
			y = self[2]*other[0]-self[0]*other[2]
			z = self[0]*other[1]-self[1]*other[0]
			return( Vec3(x,y,z))
		else:
			raise AttributeError("Vec3.cross takes an length 3 sequence")

######################################################################
# Vec4
# ====
# A 4-component vector of floats.
class Vec4(FloatVec):
	"""A four component vector"""

	# Vec4 constructor
	# ----------------
	def __init__(self, *args):
		super(Vec4, self).__init__( 4, *args)


######################################################################
# IntVec
# ========
# This is the base class for vectors with floating point elements.
# 
# It implements
# + remove and reduce (remove_and_reduce)
class IntVec(GenVec):
	"""A vector of integers, a base class for IVec2 and IVec3"""

	# IntVec constructor
	# ------------------
	def __init__(self, n, *args):
		super(IntVec,self).__init__( np.int16, n, *args)

	# reduce method
	# ------------------------
	# The vectors of integers often hold indices that point to list of
	# vertices. When you remove a vertex, you have to reorder all the
	# indices. This method allows one to very quickly do that with a
	# list comprehension
	#
	# Example:
	# >>> face_list = [IVec3[2,4,6],Ivec3[5,7,9]]
	# >>> face_list = [f.reduce(3) for f in face_list]
	# >>> face_list
	# [IVec([2,3,5]), IVec([4,6,8])]
	def reduce(self, k):
		"""reduces all number greater or equal to `k` by 1"""
		def ifshift( k, n):
			if n >= k:
				return( n-1)
			else:
				return( n)
		return( self.__class__( [ifshift(k,i) for i in self]))


######################################################################
# IVec2
# =====
# A 2-component vector of integers.
class IVec2(IntVec):
	"""A two component vector of integers"""

	# IVec2 constructor
	# ------------------
	def __init__(self, *args):
		super(IVec2, self).__init__( 2, *args)


######################################################################
# IVec3
# =====
# A 3-component vector of integers.
class IVec3(IntVec):
	"""A three component vector of integers"""

	# IVec3 constructor
	# ------------------
	def __init__(self, *args):
		super(IVec3, self).__init__( 3, *args)


######################################################################
# IVec4
# =====
# A 4-component vector of integers.
class IVec4(IntVec):
	"""A four component vector of integers"""

	# IVec4 constructor
	# ------------------
	def __init__(self, *args):
		super(IVec4, self).__init__( 4, *args)
