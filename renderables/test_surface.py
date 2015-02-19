# Author: Jef Wagner
# Date: 20-02-2015

import unittest

class TestSurface(unittest.testcase):

  def test_Face(self):
    v = []
    v.append(Vec3(0,0,0))
    v.append(Vec3(1,0,0))
    v.append(Vec3(1,0,0))
    f = Face(0,1,2)
    self.assertIsInstance(f, Face)

  def test_Constructor( self):
    v = [[-1,-1,0],
         [1,-1,0],
         [1,1,0],
         [-1,1,0],
         [0,0,1]]
    f = [[0,1,4],
         [1,2,4],
         [2,3,4],
         [3,0,4]]
    s = Surface(v,f)
    self.assertIsInstance(s, Surface)

if __name__ == '__main__':
  unittest.main()