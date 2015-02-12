# Author: Jef Wagner
# Date: 10-02-2015

import numpy as np
import numbers

class GenVec:
	"""General vector object, only used as a base class for Vec2,
	Vec3, Vec4, IVec2, IVec3"""

	def __init__(self, type, n, *args):
		"""
		Constructor for the GenVec class.
			usage: GenVec( np.int16, 4, [0,0,0,0])
				- first argument is a numpy data type
				- second argument is the size
				- following argument(s) is(are) the data.
		"""
		array = np.array( args, dtype=type).flatten()
		if len(array) == n:
			self.array = array
		else:
			raise AttributeError("{}.__init__ takes an array of length {}".format(self.name, n))

	def __len__(self):
		"""Length of the vector"""
		return( len(self.array))

	def __getitem__(self, index):
		"""
		Defines the square bracket operator.
			examples: if `vec` is an instance of GenVec 
				`vec[0]` returns for first element
				`vec[1:2]` returns a slice from the 2nd to 3rd elements
				`vec[:]` returns a slice of all elements
		"""
		return( self.array[index])

	def __iter__(self):
		"""
		Defines the behavior in for loops
			example: if `vec` is an instance of GenVec
				for x in vec:
					print( x)
		"""
		return( iter(self.array))

	def __repr__(self):
		"""
		Defines the behavior when object is printed or shown on the
		interactive command line.
			example: 
				>>> vec = IVec3( 0, 0, 1); vec
				IVec3([0, 0, 1])
		"""
		name = self.__class__.__name__
		return "{}({})".format(name,[x for x in self])

	def __neg__(self):
		"""Negative of all elements of the vector"""
		return( self.__class__([-x for x in self]))

	def __add__(self, other):
		"""
		Defines the `+` operator for scalars and sequence types 
			example:
				>>> A = Vec2(0,1)
				>>> B = A+1; B
				Vec2([1.0,2.0])
				>>> C = b+[1,-1]; C
				Vec2([2.0,1.0])
		"""
		if isinstance( other, numbers.Number):
			return( self.__class__([x+other for x in self]))
		else:
			array = np.array( other, dtype=self.array.dtype).flatten()
			if len(array) == len(self):
				return( self.__class__([x+y for x,y in zip(self,array)]))
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__add__ takes a scalar or an array with {} elements".format(name, len(self)))

	__radd__ = __add__

	def __sub__(self, other):
		"""
		Defines the `-` operator for scalars and sequence types 
		"""
		if isinstance( other, numbers.Number):
			return( self.__class__([x-other for x in self]))
		else:
			array = np.array( other, dtype=self.array.dtype).flatte()
			if len(array) == len(self):
				return( self.__class__([x-y for x,y in zip(self,array)]))
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__sub__ takes a scalar or an array with {} elements".format(name, len(self)))

	def __rsub__(self, other):
		"""
		Defines the `-` operator for scalars and sequence types 
		"""
		if isinstance( other, numbers.Number):
			return( self.__class__([other-x for x in self]))
		else:
			array = np.array( other, dtype=np.dtype(self.array)).flatte()
			if len(array) == len(self):
				return( self.__class__([y-x for x,y in zip(self,array)]))
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__sub__ takes a scalar or an array with {} elements".format(name, len(self)))

	def __mul__(self, other):
		"""
		Defines the `*` operator for scalars 
		"""
		if isinstance( other, number.Number):
			return( self.__class__([x*other for x in self]))
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.__mul__ takes a scalar".format(name))

	__rmul__ = __mul__

	def __truediv__(self, other):
		"""
		Defines the `/` operator for scalars 
		"""
		if isinstance(other, numbers.Number):
			return( self.__class__([x/other for x in self]))
		else:
			raise AttributeError("{}.__truediv__ takes a scalar".format(name))

class FloatVec(GenVec):
	"""A vector of floats, a base class for Vec2, Vec3, and Vec4"""

	def __init__(self, n, *args):
		super(FloatVec,self).__init__(np.float32, n, *args)

	def inner(self, other):
		"""Defines the inner product for two equal length sequences"""
		if len(self) == len(other):
			return( sum([x*float(y) for x, y in zip(self,other)]))
		else:
			name = self.__class__.__name__
			raise AttributeError("{}.inner takes a length {} sequence".format(name,len(self)))

	def __mul__(self, other): 
		"""
		Overloads the `*` operator to either give scalar multiplication, 
		or the inner product
		""" 
		if isinstance(other, numbers.Number): 
			return( self.__class__([x*other for x in self])) 
		else: 
			return( self.inner(other))

	__rmul__ = __mul__

	def mag(self):
		"""Defines the magnitude of a vector"""
		return( np.sqrt(self.inner(self)))

	def unit(self):
		"""Defines the unit vector in the same direction"""	
		l = self.mag()
		if l != 0:
			return( self/l)
		else:
			name = self.__class__.__name__
			raise ValueError("{}.unit does not work for the 0 vector".format(name))

class Vec2(FloatVec):
	"""A two component vector"""

	def __init__(self, *args):
		super(Vec2, self).__init__(2, *args)

	def cross(self, other):
		"""Defines the 2-d cross product, returns a scalar"""
		if len(other) == 2:
			return( self[0]*other[1]-self[1]*other[0])
		else:
			raise AttributeError("Vec2.cross takes a length 2 sequence")

class Vec3(FloatVec):
	"""A three component vector"""

	def __init__(self, *args):
		super(Vec3, self).__init__( 3, *args)

	def cross(self, other):
		"""Defines the 3-d cross product, returns another Vec3"""
		if len(other) == 3:
			x = self[1]*other[2]-self[2]*other[1]
			y = self[2]*other[0]-self[0]*other[2]
			z = self[0]*other[1]-self[1]*other[0]
			return( Vec3(x,y,z))
		else:
			raise AttributeError("Vec3.cross takes an length 3 sequence")

class Vec4(FloatVec):
	"""A four component vector"""

	def __init__(self, *args):
		super(Vec4, self).__init__( 4, *args)

class IntVec(GenVec):
	"""A vector of integers, a base class for IVec2 and IVec3"""

	def __init__(self, n, *args):
		super(IntVec,self).__init__( np.int16, n, *args)

	def remove_and_reduce(self, k):
		"""reduces all number greater than `k` by 1"""
		def ifshift( k, n):
			if k >= n:
				return( n-1)
			else:
				return( n)
		return( self.__class__( [ifshift(k,i) for i in self]))

class IVec2(IntVec):
	"""A two component vector of integers"""

	def __init__(self, *args):
		super(IVec2, self).__init__( 2, *args)

class IVec3(IntVec):
	"""A three component vector of integers"""

	def __init__(self, *args):
		super(IVec3, self).__init__( 3, *args)

class IVec4(IntVec):
	"""A four component vector of integers"""

	def __init__(self, *args):
		super(IVec4, self).__init__( 4, *args)
