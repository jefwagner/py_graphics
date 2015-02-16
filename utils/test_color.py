# Author: Jef Wagner
# Date: 15-02-2015

from color import *
from numpy import fabs

import unittest

class TestColorFunctions(unittest.TestCase):

  # Test various ways of declaring functions
  # - constructor
  # - RGB function wrapper
  # - dRGB function
  # - grayscale function
  def test_color(self):
    c = RGBA(1,1,1,1)
    self.assertIsInstance(c, RGBA)
    self.assertRaises( ValueError, RGBA, 2,1,1,1)
    c = RGB(1,1,1)
    self.assertIsInstance(c, RGBA)
    self.assertRaises( ValueError, RGB, -1,0,0)
    c = dRGB(225,225,225)
    self.assertIsInstance(c, RGBA)
    self.assertRaises( ValueError, dRGB, 285,225,300)
    c = grayscale(0.1)
    self.assertIsInstance(c, RGBA)
    self.assertRaises( ValueError, grayscale, 1.2)

  # Test two named function
  # - Test that the named functions are proper RGBA objects
  # - Test values
  def test_named_colors(self):
    self.assertIsInstance( Pink, RGBA)
    self.assertEqual( Red[0], 1)
    self.assertEqual( Red[1], 0)

  # Test color methods
  # - darken
  # - lighten
  # - opacify
  # - transparentize
  def test_color_methods(self):
    c = Red.darken()
    self.assertTrue( fabs( c[0] - 0.8)< 1.e-4 )
    c = Red.darken( 0.4)
    self.assertTrue( fabs( c[0] - 0.6)< 1.e-4 )
    c = Red.lighten()
    self.assertTrue( fabs( c[1] - 0.2)< 1.e-4 )
    c = Red.lighten( 0.4)
    self.assertTrue( fabs( c[1] - 0.4)< 1.e-4 )
    c = RGBA(0.8, 0.8, 0.8, 0).opacify()
    self.assertTrue( fabs( c[3] - 0.2)< 1.e-4 )
    c = RGBA(0.8, 0.8, 0.8, 0).opacify(0.4)
    self.assertTrue( fabs( c[3] - 0.4)< 1.e-4 )
    c = Red.transparentize()
    self.assertTrue( fabs( c[3] - 0.8)< 1.e-4 )
    c = Red.transparentize(0.4)
    self.assertTrue( fabs( c[3] - 0.6)< 1.e-4 )
    self.assertRaises( ValueError, Red.transparentize, 2)

if __name__ == '__main__':
  unittest.main()