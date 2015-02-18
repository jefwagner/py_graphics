# Author: Jef Wagner
# Date: 14-02-2015

import numpy as np

from py_graphics.utils.vector import IVec2, IVec3
from py_graphics.renderables.renderable import RenderableGraphicsObj

__all__ = ['Face','Surface']

#####################################################################
# Face class
# ==========
# A face is a triagonal piece of a larger surface. The face class is
# simply 3-vector of integers which holds the indices of the vertices
# that make up the corners of the triangles. In addition to what the
# `IVec3` class provides, it provides:
# - The vertices (calc_vertices)
# - The area center of mass (calc_center)
# - The total area (area)
# - The normal vector to the face (normal)
class Face(IVec3):

  # calc_vertices pts
  # -----------------
  # Returns the positions of the corners of the triangular face. Takes 
  # additional arguments of the list of vertices and the translation 
  # matrix. Returns a tuple of Vec3s.
  def calc_vertices(self, vertices, trans_mat)):
    """Returns the corner points of the face"""
    pt0 = trans_mat*vertices[self[0]]
    pt1 = trans_mat*vertices[self[1]]
    pt2 = trans_mat*vertices[self[2]]
    return( pt0, pt1, pt2)    

  # calc_center method
  # ---------------------
  # Returns a point the represents the area center of mass of the
  # face. It is simply the centroid of the triangle, which is simply
  # the average of the corner points.
  def calc_center(self, vertices, trans_mat):
    pt0, pt1, pt2 = self.calc_vertices( vertices, trans_mat)
    return( (pt0+pt1+pt2)/3.)

  # calc_area method
  # -----------
  # Returns the surface area of the face. The area is calculated as
  # the cross product of the vectors along two sides. The magnitude
  # of the cross product is the area of the parallelgram made up of
  # two vectors. The triangle is half that area.
  def calc_area(self, vertices, trans_mat):
    pt0, pt1, pt2 = self.calc_vertices( vertices, trans_mat)
    n = pt0.cross(pt1) + pt1.cross(pt2) + pt2.cross(pt0)
    return( 0.5*n.mag())

  # calc_normal method
  # -------------
  # Returns the normal vector to the surface of the triagular face.
  # The "top" side of the triangle is determined by looping over the 
  # corners in a counterclockwise direction. The normal is calculated
  # by taking the cross product of the two vectors along the sids,
  # then taking the unit vector in that direction.
  def calc_normal(self, vertices, trans_mat):
    pt0, pt1, pt2 = self.calc_vertices( vertices, trans_mat)
    n = pt0.cross(pt1) + pt1.cross(pt2) + pt2.cross(pt0)
    return( n.unit())


#####################################################################
# Surface class
# =============
# This class defines a smooth surface. It holds a list of vertices and
# faces. The vertices is a list of Vec3 objects, and the faces is a 
# list of Face objects. It provides the following methods:
# - Calculate area of each face (gen_face_areas)
# - Calculate the center of mass of each face (gen_face_calc_center)
# - Calculate the normal of each face (gen_face_normals)
# - Calculate the normal of each vertex (gen_vertex_normals)
# - Caclulate the total area center of mass (calc_center)
# - Calculate the total surface area (area)
class Surface(RenderableGraphicsObj):

  # Accepts the following style options:
  # - color: The diffusive color of the object
  # - specular color: The specular color of the object
  # - specularity: The sharpness of the specular highlights
  # - vertex_colors: Also possible to specify a per-vertex color
  graphics_options = ['color',
                      'specular_color',
                      'specularity',
                      'vertex_colors']

  # Surface constructor
  # -------------------
  # This constructor takes 2 or 3 positional arguments and set of 
  # keyword arguments:
  # - vertices: a sequence of vertex positions
  # - faces: a sequence of length-3 sequence of integers
  # - trans: an optional list of transformations
  # - **kwargs: a set of style parameters specified by keywords 
  #
  # The vertices argument should be a list of length-3 sequence of
  # numbers. Each element of the list is used to create a Vec3 object,
  # which represents the position of that vertex in 3-D space.
  #
  # The faces arguments should be a list of length-3 sequence of
  # integers. Each element of the list is used to create a Face
  # object. The integers in the Face object corresponds to the  the
  # index in the vertices list. The constructor checks that each
  # integer in the face arguments is less than length of the vertices
  # list, if not it raises an exception.
  #
  # In addition if any vertex is not referenced in the face list, it
  # is removed from vertices list, and the face indices are re-
  # orgnized.  
  #
  # The transforms list and style options are passed on to the parent
  # classes constructor.
  def __init__(self, vertices, faces, trans=[], **kwargs):
    """Constructor for the Surface class"""
    # Add all vertices to self.vertices as Vec3 objects
    self.vertices = []
    for v in vertices:
      self.vertices.append( Vec3(v))
    # Find max possible index, create an empty set of all indices,
    # create an empty list of faces
    max_index = len(self.vertices)-1:
    index_set = set()
    self.faces = []
    for f in faces:
      for index in f:
        # Check that index points to a vertex
        if index > max_index:
          raise AttributeError("Face({}) references index {}, which is not in the vertex list".format(f,index))
        # Add that index to an index_set
        index_set.add(index)
      # Add faces to self.faces as Face objects
      self.faces.append( Face(f))
    # From the back of the list, if the index in not reference,
    # then remove it from the index list, and shift down the indices
    # in the face list.
    for index in reversed(range(max_index+1)):
      if index not in index_set:
        self.vertices.pop(index)
        self.faces = [f.reduce(index) for f in self.faces]
    super(Surface, self).__init__(trans, **kwargs)

  # calc_face_areas method
  # ---------------------
  # This method returns a list of surface areas for each face in the 
  # faces list.
  def calc_face_areas(self):
    """Returns the area of each face"""
    face_areas = [f.calc_area(self.vertices, self.trans_mat) for f in self.faces]
    return( face_areas)

  # calc_face_centers method
  # --------------------------------
  # This method returns a list of area center of mass for each face in
  # the  faces list. 
  def calc_face_centers(self):
    """Returns the center of each face"""
    face_centers = [f.calc_center(self.vertices, self.trans_mat) for f in self.faces]
    return( face_centers)

  # calc_face_normals method
  # --------------------------------
  # This method returns a list of normal vectors for each face in
  # the  faces list. 
  def calc_face_normals(self):
    """Returns the normal vectors for each face"""
    face_normals = [f.calc_normal(self.vertices, self.trans_mat) for f in self.faces]
    return( face_normals)

  # calc_vertex_normals method
  # --------------------------
  # This method returns a list of normal vectors for each vertex. The
  # normal vectors are calculated an area weighted average of each
  # face normal.
  def calc_vertex_normals(self):
    """Returns normal vectors for each of the vertices"""
    vertex_normals = [None]*len(self.vertices)
    weights = [None]*len(self.vertices)
    fns = self.calc_face_normals()
    areas = self.calc_face_areas()
    for (f, fn, a) in zip(self.faces, fns, areas):
      for index in f:
        if vertex_normals[index] == None:
          vertex_normals[index] = fn
          weights[index] = a
        else:
          vertex_normals[index] = (weights[index]*vertex_normals[index]+a*fn)/(weights[index]+a)
          weights[index] = w[index]+a
    vertex_normals = [vn.unit() for vn in vertex_normals]
    return( vertex_normals)

  # calc_center
  # -----------
  # This method returns the surface area weighted center.
  def calc_center(self, display_radius=None):
    """Returns the center of the surface"""
    cms = self.calc_face_centers()
    areas = self.calc_face_areas()
    num = sum( [cm*area for cm, area in zip(cms, areas)])
    denom = sum( areas)
    return( num/denom)

  # calc_area
  # ---------
  # This method returns the total surface area.
  def calc_area(self, display_radius=None):
    """Returns the total surface area"""
    areas = self.calc_face_areas()
    return( sum(areas))

  # calc_vertices
  # -------------
  # This method returns all the vertices in the surface.
  def calc_vertices(self):
    """Returns a list of vertices"""
    return( self.vertices)

  # cald_vertex_attr
  # ----------------
  # This method returns a list of attributes for each vertex.
  def calc_vertex_attr(self, attr, default):
    """Returns a list of attribute values for each vertex"""
      if attr == 'color' and hasattr(self, 'vertex_colors'):
        return( self.vertex_colors)
      else:
        size = len(self.vertices)
        if hasattr( self, attr):
          val = getattr(self, attr)
          return( [val]*size)
        else:
          return( [default]*size)