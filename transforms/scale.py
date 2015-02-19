# Author: Jef Wagner
# Date: 20-02-2015

import numpy as np
from ..utils.vector import Vec3
from ..utils.matrix import Mat3x4
from transform import BaseTransform
from translate import translate

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
    