# Author: Jef Wagner
# Date: 20-02-2015

import numpy as np
from ..utils.vector import Vec3
from ..utils.matrix import Mat3x4
from transform import BaseTransform

class Translate(BaseTransform):

  def __init__(self, vec):
    self.vec = Vec3(vec)

  def mat(self, obj=None):
    T = Mat3x4(1,0,0,self.vec[0],
             0,1,0,self.vec[1],
             0,0,1,self.vec[2])
    return( T)

