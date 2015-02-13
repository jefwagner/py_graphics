# Author: Jef Wagner
# Date: 13-02-2015

from matrix import *
from vector import *

import math
import unittest

class TestMatrixFunctions(unittest.TestCase):

	# Test all versions of the constructors
	# - numbers separated by commas
	# - list for each row, separated by commas
	# - a single large list
	# - a 2-d list
	# - a list with the wrong number of elements
	def test_Constructor(self):
		m = Mat2x2(1,0,0,1)
		self.assertIsInstance(m, Mat2x2)
		m = Mat3x3([1,0,0],[0,1,0],[0,0,1])
		self.assertIsInstance(m, Mat3x3)
		a = [1,0,0,0,0]*4
		m = Mat4x4(a[:16])
		self.assertIsInstance(m, Mat4x4)
		a = [1,0,0,0]*3
		a = [a[i:i+3] for i in range(0,len(a),3)][:2]
		m = Mat2x3(a)
		self.assertIsInstance(m, Mat2x3)
		a = [0]*30
		self.assertRaises( AttributeError, Mat3x4, a)

	# Test the len function for all objects
	# note that this returns the number of rows
	def test_len(self):
		ml = [ Mat2x2([0]*4),
			   Mat3x3([0]*9),
			   Mat4x4([0]*16),
			   Mat2x3([0]*6),
			   Mat3x4([0]*12)]
		l = [len(m) for m in ml]
		self.assertEqual( l, [2,3,4,2,3])

	# Test the `[]` operator for elements, slices, 
	# and the __iter__ command for iteration.
	# The slice returns a numpy array, and equiivalence testing
	# returns an array of bools, so I have to use the built in
	# `all` function. Further, the iteration should itterate
	# over rows.
	def test_index_and_iter(self):
		m = Mat2x2(1,2,3,4)
		self.assertEqual(m[0,0],1)
		m = Mat3x3(1,2,3,4,5,6,7,8,9)
		self.assertTrue( all( m[0,:] == [1,2,3]))
		self.assertTrue( all( m[:,0] == [1,4,7]))
		column1 = [row[1] for row in m]
		self.assertEqual( column1, [2,5,8])

	# Test the formatting with direct comparison
	def tests_repr(self):
		m = Mat2x3(range(6))
		repr_str = m.__repr__()
		result = "Mat2x3([[0.0, 1.0, 2.0],\n        [3.0, 4.0, 5.0]])"
		self.assertEqual( repr_str, result)

	# Test the equality, inequality, and closeness
	def test_equal_and_close(self):
		m = Mat2x3([0]*6)
		self.assertEqual( m, [[0,0,0],[0,0,0]])
		m = Mat2x2([1,0],[0,1])
		self.assertNotEqual( m, [[1,0],[0,1.01]])
		m = Mat4x4([0]*16)
		self.assertRaises( AttributeError, m.__eq__, range(16))
		m2 = [[1.e-10, 1.e-10, 1.e-10,0] for x in range(4)]
		self.assertTrue( m.close( m2))

	# Test the dot product, and the redefined multiplication
	# routines. This uses a Vec2 from the vector module to test
	# matrix vector dot product as well.
	def test_dot_and_mul(self):
		eye = Mat2x2(1,0,0,1)
		m = Mat2x2(0,-1,1,0)
		self.assertEqual( m*m*m*m, eye)
		v = Vec2(1,0)
		self.assertEqual( m*v, [0,1])
		m = Mat2x3(1,0,1,0,1,1)
		self.assertEqual( m*v, [1,2])
		self.assertEqual( m*m, [[1,0,2],[0,1,2]])
		m2 = Mat3x3([0]*9)
		self.assertRaises( AttributeError, m.dot, m2)

	# This test the matrix inversion. Because of round off error
	# the matrix times its inverse is not quite the identity, so
	# we make the comparison with the `close` method.
	def test_inv(self):
		eye3 = Mat3x3(1,0,0,0,1,0,0,0,1)
		eye34 = Mat3x4(1,0,0,0,0,1,0,0,0,0,1,0)
		m = Mat3x3([(x+1)**2 for x in range(9)])
		self.assertTrue( (m*m.inv()).close( eye3, 1.e-3, 1.e-4))
		m = Mat3x4([(x+1)**2 for x in range(12)])
		self.assertTrue( (m*m.inv()).close( eye34, 1.e-3, 1.e-4))

	# Test turning an affine matrix into a square matrix.
	def test_tosquare(self):
		self.assertIsInstance(Mat3x4([0]*12).to_square(), Mat4x4)
		self.assertIsInstance(Mat2x3([0]*6).to_square(), Mat3x3)

if __name__ == '__main__':
	unittest.main()