# Author: Jef Wagner
# Date: 20-02-2015

import numpy as np
from ..utils.vector import Vec3
from ..utils.matrix import Mat3x4
from transform import BaseTransform
from translate import translate

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