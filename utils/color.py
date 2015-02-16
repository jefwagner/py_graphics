# Author: Jef Wagner
# Date: 14-02-2015

from vector import BaseVec
import numpy as np

##################################################################
# RGBA Class
# ==========
# This class is a wrapper around a 4-vector of floats to hold the
# red, green, blue, and alpha channels. All values are limited to
# values between 0 and 1. The class provides:
# - Darken the color by 20% (darken)
# - Lighten the color by 20% (lighten)
# - Make the color more opaque by 20% (opacify)
# - Make the color more transparent by 20% (transparentize)
class RGBA(BaseVec):
  """Color objects with a red, gree, blue, and alpha channels"""

  # __init__ method
  # ---------------
  # This simply checks that all values are between 0 and 1.
  def __init__(self, *args):
    """Constructor of the RGBA class"""
    super(RGBA, self).__init__(np.float32, 4, *args)
    for c in self:
      if not (0 <= c <= 1):
        raise ValueError("All color components must be between 0 and 1")

  # darken method
  # -------------
  # This reduces the value of the red, green, and blue channels.
  def darken(self, percent=None):
    """Returns a darker shade of the color"""
    if percent != None:
      if not (0 <= percent <= 1):
        raise ValueError("The parameter must be between 0 and 1")
      v = 1-percent
    else:
      v = 0.8 
    r,g,b = [v*c for c in self[:3]]
    a = self[3]
    return( RGBA(r,g,b,a))
  
  # lighten method
  # --------------
  # This increases the value of the red, gree, and blue channels.
  def lighten(self, percent=None):
    """Returns a color that is 20 percent lighter"""
    if percent != None:
      if not (0 <= percent <= 1):
        raise ValueError("The parameter must be between 0 and 1")
      v = 1-percent
    else:
      v = 0.8 
    r,g,b = [1-v*(1-c) for c in self[:3]]
    a = self[3]
    return( RGBA(r,g,b,a))

  # opacify method
  # --------------
  # This increases the value of the alpha channel.
  def opacify(self, percent=None):
    """Returns a color that is more opaque"""
    if percent != None:
      if not (0 <= percent <= 1):
        raise ValueError("The parameter must be between 0 and 1")
      v = 1-percent
    else:
      v = 0.8 
    r,g,b = self[:3]
    a = 1-v*(1-self[3])
    return( RGBA(r,g,b,a))

  # transparentize method
  # ---------------------
  # This decreases the value of teh alpha channel.
  def transparentize(self, percent=None):
    """Returns a color that is more transparent"""
    if percent != None:
      if not (0 <= percent <= 1):
        raise ValueError("The parameter must be between 0 and 1")
      v = 1-percent
    else:
      v = 0.8 
    r,g,b = self[:3]
    a = v*self[3]
    return( RGBA(r,g,b,a))

# RGB function
# ------------
# An opaque color with given red, green, and blue channels, with the
# alpha channel set to 1.
def RGB(r, g, b):
  """Returns a color object with alpha=1"""
  return( RGBA(r, g, b, 1))

# dRGB function
# -------------
# An opaque color with red, green, and blue channels between with 
# values between 0 and 255. The alpha channel is set to 1
def dRGB(r, g, b):
  """Returns a color object with r,g, and b values between 0 and 255"""
  for c in (r,g,b):
    if not 0 <= c <= 255:
      raise ValueError("All color components must be between 0 and 255")
  return( RGBA(r/255, g/255, b/255, 1))

# grayscale function
# -------------------
# Boo
def grayscale( n):
  if not (0 <= n <= 1):
    raise ValueError("All color components must be betwen 0 and 1")
  return( RGBA(n,n,n,1))


####################################################################
# Named Colors
# ============
# These are named colors using the css3 naming scheme. These values
# were taken from the wikipedia article.
Pink = RGBA( 255/255, 192/255, 203/255, 1)
LightPink = RGBA( 255/255, 182/255, 193/255, 1)
HotPink = RGBA( 255/255, 105/255, 180/255, 1)
DeepPink = RGBA( 255/255, 20/255, 147/255, 1)
PaleVioletRed = RGBA( 219/255, 112/255, 147/255, 1)
MediumVioletRed = RGBA( 199/255, 21/255, 133/255, 1)
LightSalmon = RGBA( 255/255, 160/255, 122/255, 1)
Salmon = RGBA( 250/255, 128/255, 114/255, 1)
DarkSalmon = RGBA( 233/255, 150/255, 122/255, 1)
LightCoral = RGBA( 240/255, 128/255, 128/255, 1)
IndianRed = RGBA( 205/255, 92/255, 92/255, 1)
Crimson = RGBA( 220/255, 20/255, 60/255, 1)
FireBrick = RGBA( 178/255, 34/255, 34/255, 1)
DarkRed = RGBA( 139/255, 0/255, 0/255, 1)
Red = RGBA( 255/255, 0/255, 0/255, 1)
OrangeRed = RGBA( 255/255, 69/255, 0/255, 1)
Tomato = RGBA( 255/255, 99/255, 71/255, 1)
Coral = RGBA( 255/255, 127/255, 80/255, 1)
DarkOrange = RGBA( 255/255, 140/255, 0/255, 1)
Orange = RGBA( 255/255, 165/255, 0/255, 1)
Yellow = RGBA( 255/255, 255/255, 0/255, 1)
LightYellow = RGBA( 255/255, 255/255, 224/255, 1)
LemonChiffon = RGBA( 255/255, 250/255, 205/255, 1)
LightGoldenrodYellow = RGBA( 250/255, 250/255, 210/255, 1)
PapayaWhip = RGBA( 255/255, 239/255, 213/255, 1)
Moccasin = RGBA( 255/255, 228/255, 181/255, 1)
PeachPuff = RGBA( 255/255, 218/255, 185/255, 1)
PaleGoldenrod = RGBA( 238/255, 232/255, 170/255, 1)
Khaki = RGBA( 240/255, 230/255, 140/255, 1)
DarkKhaki = RGBA( 189/255, 183/255, 107/255, 1)
Gold = RGBA( 255/255, 215/255, 0/255, 1)
Cornsilk = RGBA( 255/255, 248/255, 220/255, 1)
BlanchedAlmond = RGBA( 255/255, 235/255, 205/255, 1)
Bisque = RGBA( 255/255, 228/255, 196/255, 1)
NavajoWhite = RGBA( 255/255, 222/255, 173/255, 1)
Wheat = RGBA( 245/255, 222/255, 179/255, 1)
BurlyWood = RGBA( 222/255, 184/255, 135/255, 1)
Tan = RGBA( 210/255, 180/255, 140/255, 1)
RosyBrown = RGBA( 188/255, 143/255, 143/255, 1)
SandyBrown = RGBA( 244/255, 164/255, 96/255, 1)
Goldenrod = RGBA( 218/255, 165/255, 32/255, 1)
DarkGoldenrod = RGBA( 184/255, 134/255, 11/255, 1)
Peru = RGBA( 205/255, 133/255, 63/255, 1)
Chocolate = RGBA( 210/255, 105/255, 30/255, 1)
SaddleBrown = RGBA( 139/255, 69/255, 19/255, 1)
Sienna = RGBA( 160/255, 82/255, 45/255, 1)
Brown = RGBA( 165/255, 42/255, 42/255, 1)
Maroon = RGBA( 128/255, 0/255, 0/255, 1)
DarkOliveGreen = RGBA( 85/255, 107/255, 47/255, 1)
Olive = RGBA( 128/255, 128/255, 0/255, 1)
OliveDrab = RGBA( 107/255, 142/255, 35/255, 1)
YellowGreen = RGBA( 154/255, 205/255, 50/255, 1)
LimeGreen = RGBA( 50/255, 205/255, 50/255, 1)
Lime = RGBA( 0/255, 255/255, 0/255, 1)
LawnGreen = RGBA( 124/255, 252/255, 0/255, 1)
Chartreuse = RGBA( 127/255, 255/255, 0/255, 1)
GreenYellow = RGBA( 173/255, 255/255, 47/255, 1)
SpringGreen = RGBA( 0/255, 255/255, 127/255, 1)
MediumSpringGreen = RGBA( 0/255, 250/255, 154/255, 1)
LightGreen = RGBA( 144/255, 238/255, 144/255, 1)
PaleGreen = RGBA( 152/255, 251/255, 152/255, 1)
DarkSeaGreen = RGBA( 143/255, 188/255, 143/255, 1)
MediumSeaGreen = RGBA( 60/255, 179/255, 113/255, 1)
SeaGreen = RGBA( 46/255, 139/255, 87/255, 1)
ForestGreen = RGBA( 34/255, 139/255, 34/255, 1)
Green = RGBA( 0/255, 128/255, 0/255, 1)
DarkGreen = RGBA( 0/255, 100/255, 0/255, 1)
MediumAquamarine = RGBA( 102/255, 205/255, 170/255, 1)
Aqua = RGBA( 0/255, 255/255, 255/255, 1)
Cyan = RGBA( 0/255, 255/255, 255/255, 1)
LightCyan = RGBA( 224/255, 255/255, 255/255, 1)
PaleTurquoise = RGBA( 175/255, 238/255, 238/255, 1)
Aquamarine = RGBA( 127/255, 255/255, 212/255, 1)
Turquoise = RGBA( 64/255, 224/255, 208/255, 1)
MediumTurquoise = RGBA( 72/255, 209/255, 204/255, 1)
DarkTurquoise = RGBA( 0/255, 206/255, 209/255, 1)
LightSeaGreen = RGBA( 32/255, 178/255, 170/255, 1)
CadetBlue = RGBA( 95/255, 158/255, 160/255, 1)
DarkCyan = RGBA( 0/255, 139/255, 139/255, 1)
Teal = RGBA( 0/255, 128/255, 128/255, 1)
LightSteelBlue = RGBA( 176/255, 196/255, 222/255, 1)
PowderBlue = RGBA( 176/255, 224/255, 230/255, 1)
LightBlue = RGBA( 173/255, 216/255, 230/255, 1)
SkyBlue = RGBA( 135/255, 206/255, 235/255, 1)
LightSkyBlue = RGBA( 135/255, 206/255, 250/255, 1)
DeepSkyBlue = RGBA( 0/255, 191/255, 255/255, 1)
DodgerBlue = RGBA( 30/255, 144/255, 255/255, 1)
CornflowerBlue = RGBA( 100/255, 149/255, 237/255, 1)
SteelBlue = RGBA( 70/255, 130/255, 180/255, 1)
RoyalBlue = RGBA( 65/255, 105/255, 225/255, 1)
Blue = RGBA( 0/255, 0/255, 255/255, 1)
MediumBlue = RGBA( 0/255, 0/255, 205/255, 1)
DarkBlue = RGBA( 0/255, 0/255, 139/255, 1)
Navy = RGBA( 0/255, 0/255, 128/255, 1)
MidnightBlue = RGBA( 25/255, 25/255, 112/255, 1)
Lavender = RGBA( 230/255, 230/255, 250/255, 1)
Thistle = RGBA( 216/255, 191/255, 216/255, 1)
Plum = RGBA( 221/255, 160/255, 221/255, 1)
Violet = RGBA( 238/255, 130/255, 238/255, 1)
Orchid = RGBA( 218/255, 112/255, 214/255, 1)
Fuchsia = RGBA( 255/255, 0/255, 255/255, 1)
Magenta = RGBA( 255/255, 0/255, 255/255, 1)
MediumOrchid = RGBA( 186/255, 85/255, 211/255, 1)
MediumPurple = RGBA( 147/255, 112/255, 219/255, 1)
BlueViolet = RGBA( 138/255, 43/255, 226/255, 1)
DarkViolet = RGBA( 148/255, 0/255, 211/255, 1)
DarkOrchid = RGBA( 153/255, 50/255, 204/255, 1)
DarkMagenta = RGBA( 139/255, 0/255, 139/255, 1)
Purple = RGBA( 128/255, 0/255, 128/255, 1)
Indigo = RGBA( 75/255, 0/255, 130/255, 1)
DarkSlateBlue = RGBA( 72/255, 61/255, 139/255, 1)
RebeccaPurple = RGBA( 102/255, 51/255, 153/255, 1)
SlateBlue = RGBA( 106/255, 90/255, 205/255, 1)
MediumSlateBlue = RGBA( 123/255, 104/255, 238/255, 1)
White = RGBA( 255/255, 255/255, 255/255, 1)
Snow = RGBA( 255/255, 250/255, 250/255, 1)
Honeydew = RGBA( 240/255, 255/255, 240/255, 1)
MintCream = RGBA( 245/255, 255/255, 250/255, 1)
Azure = RGBA( 240/255, 255/255, 255/255, 1)
AliceBlue = RGBA( 240/255, 248/255, 255/255, 1)
GhostWhite = RGBA( 248/255, 248/255, 255/255, 1)
WhiteSmoke = RGBA( 245/255, 245/255, 245/255, 1)
Seashell = RGBA( 255/255, 245/255, 238/255, 1)
Beige = RGBA( 245/255, 245/255, 220/255, 1)
OldLace = RGBA( 253/255, 245/255, 230/255, 1)
FloralWhite = RGBA( 255/255, 250/255, 240/255, 1)
Ivory = RGBA( 255/255, 255/255, 240/255, 1)
AntiqueWhite = RGBA( 250/255, 235/255, 215/255, 1)
Linen = RGBA( 250/255, 240/255, 230/255, 1)
LavenderBlush = RGBA( 255/255, 240/255, 245/255, 1)
MistyRose = RGBA( 255/255, 228/255, 225/255, 1)
Gainsboro = RGBA( 220/255, 220/255, 220/255, 1)
LightGrey = RGBA( 211/255, 211/255, 211/255, 1)
Silver = RGBA( 192/255, 192/255, 192/255, 1)
DarkGray = RGBA( 169/255, 169/255, 169/255, 1)
Gray = RGBA( 128/255, 128/255, 128/255, 1)
DimGray = RGBA( 105/255, 105/255, 105/255, 1)
LightSlateGray = RGBA( 119/255, 136/255, 153/255, 1)
SlateGray = RGBA( 112/255, 128/255, 144/255, 1)
DarkSlateGray = RGBA( 47/255, 79/255, 79/255, 1)
Black = RGBA( 0/255, 0/255, 0/255, 1)
