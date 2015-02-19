# Author: Jef Wagner
# Date: 10-02-2015

import numpy as np
from ..utils.vector import Vec3
from ..utils.matrix import Mat3x4

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
		m = Mat3x4(1,0,0,0,0,1,0,0,0,0,1,0)
		for trans in self.trans_list:
			m = trans.get_mat(obj)*m
		return( m)