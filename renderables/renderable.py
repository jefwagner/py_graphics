# Author: Jef Wagner
# Date: 19-02-2015

from py_graphics.graphics import BaseGraphicsObj

##############################################################################
# Renderable Graphic Object class
# ===============================
# This class serves dual purposes, a) It acts as a base class for all
# renderable objects, b) it acts as a container for multiple multiple objects.
# It provides:
# - A constructor to combined many graphics
# - A dummy to_renderable method
# - A method for getting a list of surface vertices (calc_vertices)
# - A method for getting a list of surface vertex normals (calc_vertex_normals)
# - A method for getting a list of surface vertex attributes (calc_vertex_attr)
class RenderableGraphicsObj(BaseGraphicsObj):

	graphics_options = ['color',
						'specular_color',
						'specularity',
						'line_color',
						'line_width',
						'line_style',
						'point_color',
						'point_size',
						'point_style']

	# The RenderableGraphicsObj constructor
	# -------------------------------------
	# This takes a sequence of renderable graphics objects and creates an 
	# object list.
	def __init__( self, *args, trans=[], **kwargs):
		"""Creates a combined graphics object"""
		obj_list = []
		for obj in args:
			if isinstance(RenderableGraphicsObj, obj):
				self.obj_list.append(obj)
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__init__ takes and array of RenderableGraphicsObjs")
		super(RenderableGraphicsObjs, self).__init__(trans, **kwargs)

	# to_renderable
	# -------------
	# This is a dummy method. When `to_renderable` is called it simply returns
	# itself.
	def to_renderable(self, display_radius=None):
		return( self)

	# calc_vertices
	# -------------
	# This returns a list of vertices in the all the surfaces in all of the
	# graphics objects in the object list.
	def calc_vertices(self):
		"""Returns a list of vertices"""
		vertices = []
		for obj in self.obj_list:
			vertices = vertices + obj.calc_vertices()
		return( vertices)

	# calc_vertex_normals
	# -------------------
	# This returns a list of vertex normals in all of the surfaces in all of
	# the graphicis objects in the object list.
	def calc_vertex_normals(self):
		"""Returns a lsit of vertex normals"""
		normals = []
		for obj in self.obj_list:
			normals = normals + obj.calc_vertex_normals()
		return( normals)

	# calc_vertex_attr
	# ----------------
	# This returns a lsit of vertex attributes for each vertex in all the 
	# surfaces in all the graphics objects in the object list.
	def calc_vertex_attr(self, attr, default):
		"""Returns a list of vertex attributes"""
		attr_list = []
		if hasattr(self, attr):
			current_default = getattr(self, attr)
		else:
			current_default = default
		for obj in self.obj_list:
			attr_list += obj.calc_vertex_attr( attr, current_default)