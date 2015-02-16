# Author: Jef Wagner
# Date: 10-02-2015

import numpy as np
from vec import *
from mat import *

class BaseTransform:
	pass

class Transform(BaseTransform):

	def __init__( self, *args):
		self.trans_list = []
		for trans in args:
			if isinstance( trans, BaseTransform):
				self.trans_list.append(trans)
			else:
				raise AttributeError("Transform.__init__ takes an array of BaseTransforms")

	def get_mat(self, obj):
		m = Mat34(np.eye(3))
		for trans in self.trans_list:
			m = trans.get_mat(obj)*m
		return( m)

class Translate(BaseTransform):

	def __init__(self, vec):
		self.vec = Vec3(vec)

	def mat(self, obj=None):
		A = np.eye(3, dtype=np.float32)
		m = np.append( A, self.vec, axis=1)
		return( Mat3x4(m))

class ScaleXYZ(BaseTransform):

	def __init__(self, *args, origin=None):
		v = np.array(args, dtype=np.float32).flatten()
		if len(v) == 1:
			self.scale_vec = Vec3(v[0],v[0],v[0])
		elif len(v) == 3:
			self.scale_vec = Vec3(v)
		else:
			raise AttributeError("ScaleXYZ.__init__ takes an array with 1 or 3 elements")
		if origin == None:
			self.origin = None
		else:
			self.origin = Vec3(origin)

	def get_mat(self, obj):
		if self.origin == None:
			o = obj.center_of_mass()
		else:
			o = self.origin
		tr0 = Translate(-o).get_mat()
		tr1 = Translate(o).get_mat()
		v = self.scale_vec
		S = Mat3x4([[v[0],0,0,0],
			        [0,v[1],0,0],
			        [0,0,v[2],0]])
		return( tr1*S*tr0)		

class Shear(BaseTransform):

	def __init__(self, *args, origin=None):
		v = np.array(args, dtype=np.float32).flatten()
		if len(v) == 2: 
			self.shear_vec = v
		else:
			raise AttributeError("ShearZ.__init__ takes an array with 2 elements")
		if origin == None:
			self.origin = None
		else:
			self.origin = Vec3(origin)

class ShearX(Shear):

	def get_mat(self, obj):
		if self.origin == None:
			o = obj.center_of_mass()
		else:
			o = self.origin
		tr0 = Translate(-o).get_mat()
		tr1 = Translate(o).get_mat()
		my = self.shear_vec[0]
		mz = self.shear_vec[1]
		Sh = Mat3x4([1,0,0,0],
			        [my,1,0,0],
			        [mz,0,1,0])
		return( tr1*Sh*tr0)

class ShearY(Shear):

	def get_mat(self, obj):
		if self.origin == None:
			o = obj.center_of_mass()
		else:
			o = self.origin
		tr0 = Translate(-o).get_mat()
		tr1 = Translate(o).get_mat()
		mz = self.shear_vec[0]
		mx = self.shear_vec[1]
		Sh = Mat3x4([1,mx,0,0],
			        [0,1,0,0],
			        [0,mz,1,0])
		return( tr1*Sh*tr0)

class ShearZ(Shear):

	def get_mat(self, obj):
		if self.origin == None:
			o = obj.center_of_mass()
		else:
			o = self.origin
		tr0 = Translate(-o).get_mat()
		tr1 = Translate(o).get_mat()
		mx = self.shear_vec[0]
		my = self.shear_vec[1]
		Sh = Mat3x4([1,0,mx,0],
			        [0,1,my,0],
			        [0,0,1,0])
		return( tr1*Sh*tr0)

class Rotate(BaseTransform):

	def __init__(self, angle, origin=None):
		self.angle = float(angle)
		if origin == None:
			self.origin = None
		else:
			self.origin = Vec3(origin)

class RotateX(Rotate):

	def get_mat(self, obj):
		if self.origin == None:
			o = obj.center_of_mass()
		else:
			o = self.origin
		tr0 = Translate(-o).get_mat()
		tr1 = Translate(o).get_mat()
		a = self.angle
		R = Mat3x4([1,0,0,0],
			       [0, np.cos(a), -np.sin(a), 0],
			 	   [0, np.sin(a), np.cos(a), 0])
		return( tr1*R*tr0)

class RotateY(Rotate):

	def get_mat(self, obj):
		if self.origin == None:
			o = obj.center_of_mass()
		else:
			o = self.origin
		tr0 = Translate(-o).get_mat()
		tr1 = Translate(o).get_mat()
		a = self.angle
		R = Mat3x4([np.cos(a), 0, np.sin(a), 0],
			       [0,1,0,0],
			 	   [-np.sin(a), 0, np.cos(a), 0])
		return( tr1*R*tr0)

class RotateZ(Rotate):

	def get_mat(self, obj):
		if self.origin == None:
			o = obj.center_of_mass()
		else:
			o = self.origin
		tr0 = Translate(-o).get_mat()
		tr1 = Translate(o).get_mat()
		a = self.angle
		R = Mat3x4([np.cos(a), -np.sin(a), 0, 0],
			 	   [np.sin(a), np.cos(a), 0, 0],
			 	   [0, 0, 1, 0])
		return( tr1*R*tr0)

class RotateAA(BaseTransform):

	def __init__(self, angle, axis, origin=None):
		self.angle = float(angle)
		self.axis = Vec3(axis).unit()
		if origin == None:
			self.origin = None
		else:
			self.origin = origin

	def get_mat(self, obj):
		if self.origin == None:
			o = obj.center_of_mass()
		else:
			o = self.origin
		tr0 = Translate(-o).get_mat()
		tr1 = Translate(o).get_mat()
		ux, uy, uz = self.axis
		s = np.sin(self.angle)
		c = np.cos(self.angle)
		R = Mat3x4([c+ux*ux*(1-c), ux*uy*(1-c)-uz*s, ux*uz*(1-c)+uy*s, 0],
			       [uy*ux*(1-c)+uz*s, c+uy*uy*(1-c), uy*uz*(1-c)-ux*s, 0],
			       [yz*uz*(1-c)-uy*s, uz*uy*(1-c)+ux*s, c+uz*uz*(1-c), 0])
		return( tr1*R*tr0)
