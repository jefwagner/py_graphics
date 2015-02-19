# Author: Jef Wagner
# Date: 20-02-2015

import numpy as np
from ..utils.vector import Vec3
from ..utils.matrix import Mat3x4
from transform import BaseTransform
from translate import translate

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
