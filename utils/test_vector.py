# Author: Jef Wagner
# Date: 12-02-2015

from vector import *

import math
import unittest

class TestVectorFunctions(unittest.TestCase):

  # Test out all the constructors with all possiblitities:
  # - numbers separated by commas
  # - a list of numbers
  # - a tuple of numbers
  # - a 2-D row array of numbers
  # - a 2-D column array of numbers
  # - the wrong number of numbers (should raise exception)
  def test_Constructor(self):
    v = Vec2(0,1)
    self.assertIsInstance(v, Vec2)
    v = Vec3([0,1,2])
    self.assertIsInstance(v, Vec3)
    v = Vec4((0,1,2,3))
    self.assertIsInstance(v, Vec4)
    v = IVec2([[0,1]])
    self.assertIsInstance(v, IVec2)
    v = IVec3([[0],[1],[2]])
    self.assertIsInstance(v, IVec3)
    self.assertRaises( AttributeError, IVec4, 0)

  # Test the len function for all objects
  def test_len(self):
    vl = [Vec2(0,0),Vec3(0,0,0),Vec4(0,0,0,0),
          IVec2(0,0),IVec3(0,0,0),IVec4(0,0,0,0)]
    ll = [2,3,4,2,3,4]
    self.assertEqual([len(v) for v in vl],ll)

  # Test the [] for elements and slices,
  # The slice returns a numpy array, and equivalence testing returns 
  # an array of bools, so I have to use the `all` method.
  def test_index(self):
    element = Vec3(0,1,2)[1]
    self.assertEqual(element, 1)
    my_slice = Vec4(0,2,4,6)[1:3]
    self.assertTrue((my_slice==[2,4]).all())

  # Test iteration by using list comprehension
  def test_iter(self):
    list_comp = [i for i in IVec4(0,1,2,3)]
    self.assertEqual(list_comp, [0,1,2,3])

  # Test the formating with direct comparison known correct result.
  def test_repr(self):
    repr_str = Vec3(0,1,2).__repr__()
    self.assertEqual( repr_str, "Vec3([0.0, 1.0, 2.0])")

  # Test equality, try all combinations,
  # - between different instances of same objects
  # - between different objects of same length
  # - between vector and list
  # - between vector and tuple
  # - between vector and list of different length (raise exception)
  def test_equal(self):
    v3a = Vec3(1,2,3)
    v3b = Vec3([1,2,3])
    i3 = IVec3([[1,2,3]])
    self.assertEqual(v3a,v3b)
    self.assertEqual(v3a,i3)
    self.assertEqual(v3a,[1,2,3])
    self.assertEqual(v3b,(1,2,3))
    self.assertNotEqual(i3,[0,1,2])
    self.assertRaises( AttributeError, i3.__eq__, [0])
    self.assertRaises( AttributeError, i3.__eq__, Vec2(0,0))

  # Test overloaded arithmatic operators
  # - unary `-` operator, element wise negation
  # - bianary `+` operator, scalar addition
  # - bianary `-` operator, elementwise subtraction
  # - bianary `-` operator, elementwise left subtranction
  # - bianary `+` operator, addition with wrong size sequence (raise exception)
  # - bianary `*` operator, left scalar multiplication
  # - bianary `/` operator, right scalar division
  def test_arithmatic(self):
    self.assertEqual(-Vec4(1,2,3,4),[-1,-2,-3,-4])
    self.assertEqual(Vec3(0,1,2)+1, [1,2,3])
    self.assertEqual(IVec4(5,4,3,2)-IVec4(0,1,2,3), [5,3,1,-1])
    self.assertEqual([5,4,3]-IVec3(3,2,1), [2,2,2])
    self.assertRaises( AttributeError, IVec2(1,2).__add__, [0]*5)
    self.assertEqual(2*Vec2(1,2), [2,4])
    self.assertEqual(Vec3(3,6,9)/2, [1.5,3,4.5])

  # Test the method defined for the floating point vectors
  # - inner product
  # - inner product with different length objects (raises exception)
  # - overloaded `*` operator
  # - magnitude
  # - unit vector
  # - unit vector with 0 magnitude (raises exception)
  # - cross product for Vec2 objects
  # - cross product for Vec3 objects
  def test_float_methods(self):
    self.assertEqual(Vec3(1,2,3).inner([0,1,2]), 8)
    self.assertRaises( AttributeError, Vec2(1,2).inner, [0,1,2])
    self.assertEqual(Vec2(2,3)*Vec2(1,2), 8)
    self.assertEqual(Vec4(1,1,1,1).mag(), math.sqrt(4))
    self.assertEqual(Vec2(3,4).unit(), Vec2(0.6,0.8))
    self.assertRaises( ValueError, Vec2(0,0).unit )
    self.assertEqual( Vec2(1,0).cross(Vec2(0,1)), 1)
    self.assertEqual( Vec3(1,0,0).cross((0,1,0)), Vec3(0,0,1))

  # Test the methods defined for integer vectors
  # - remove and reduce
  def test_integer_methods(self):
    face_list = [IVec3([2,4,6]),IVec3([5,7,9])]
    face_list = [iv.reduce(3) for iv in face_list]
    self.assertEqual( face_list, [(2,3,5),(4,6,8)])

if __name__ == '__main__':
  unittest.main()