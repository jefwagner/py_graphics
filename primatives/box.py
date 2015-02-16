# Author: Jef Wagner
# Date: 10-02-2015

class Box(PrimativeGrpahicsObj):
	"""A cuboid aligned with the x, y, z axis before transforms"""

	graphics_options = ['color', # Diffusive surface color
						'ambient_color', # Ambient surface color
						'specular_color', # Specular surface color
						'specularity', # Shinyness for surface in Phong Model
						'face_colors', # Each face a different color
						'line_color', # Line color
						'line_width', # Line width
						'line_style', # Line style
						'edge_colors', # Each edge a different color
						'point_color', # Point color for the corners
						'point_size', # Point size for the corners
						'point_style' # Point style for the corners
						'vertex_colors'] # Gradient color between the vertices
	# Note: The vertex color arguments overrides the color argument for the
	# surface, line, and points.

	def __init__(self, pt0, pt1=Vec3([0,0,0]), transforms=[], **kwargs):
		"""Constructor takes 1 or 2 points."""
		self.pt0 = Vec3(pt0)
		self.pt1 = Vec3(pt1)
		super(Box,self).__init__(transforms,**kwargs)

	def gen_vertices():
		"""Calculate the vertices for the box in the untransformed coordinates"""
		if not hasattr(self, 'vertices'):
			x0, y0, z0 = self.pt0 # Front Left Bottom
			x1, y1, z1 = self.pt1 # Back Right Top
			self.vertices = [ Vec3(x0,y0,z0), # Front Left Bottom
		    	  			  Vec3(x1,y0,z0), # Back Left Bottom
			      			  Vec3(x1,y1,z0), # Back Right Bottom
			      			  Vec3(x0,y1,z0), # Front Right Bottom
			      			  Vec3(x0,y0,z1), # Front Left Top
		    	  			  Vec3(x1,y0,z1), # Back Left Top
			      			  Vec3(x1,y1,z1), # Back Right Top
		    	  			  Vec3(x0,y1,z1)] # Front Right Top
		return( self.vertices)

	def gen_edges():
		"""Calculate the edges for the cuboid"""
		if not hasattr(self, 'edges'):
			self.edges = [ Edge(0,1), Edge(1,2), Edge(2,3), Edge(3,0), # Bottom edges
			          	   Edge(0,4), Edge(1,5), Edge(2,6), Edge(3,7), # Side edges
			          	   Edge(4,5), Edge(5,6), Edge(6,7), Edge(7,4)] # Top edges
		return( self.edges)

	def gen_faces():
		"""Calculate the faces for the cuboid"""
		if not hasattr(self, 'faces'):
			self.faces = [ Face(0,1,2), Face(0,2,3), # Bottom face
						   Face(0,4,5), Face(0,5,1), # Front face
						   Face(1,5,6), Face(1,6,2), # Left face
						   Face(2,6,7), Face(2,7,3), # Back face
						   Face(3,7,4), Face(3,4,0), # Right face
						   Face(4,6,5), Face(4,7,6)] # Top face
		return( self.faces)

	def center_of_mass(self, display_radius):
		"""Calculate the area center of mass of the box"""
		return( self.trans_mat(0.5*(self.pt0+self.pt1)))

	def area(self, display_radius = None):
		"""Calculate the total surface area of the box"""
		area = 0
		if hasattr(self, 'point_size') or hasattr(self, 'point_style') or hasattr(self, 'point_color'):
			dx = calc_dx_from_point_size( self.point_size, display_radius)
			area += 8*dx*dx
		vertices = self.gen_vertices()
		if hasattr(self, 'line_width') or hasattr(self, 'line_style') or hasattr(self, 'line_color'):
			dx = calc_dx_from_line_width( self.line_width, display_radius)
			length = sum( [e.length(vertices, self.trans_mat) for e in self.gen_edges()])
			area += dx*length
		sum( [f.area(vertices, self.trans_mat) for f in self.gen_faces()])

	def to_renderable(self, display_radius = None):
		"""Convert the box to a RenderableGraphicsObject"""
		vertices = self.gen_vertices()
		faces = self.gen_faces()
		objs = []
		style_options = self.get_style_options()
		# Only add points to the graphics objects if one of the point options
		# is specified
		# if hasattr(self, 'point_size') or hasattr(self, 'point_style') or hasattr(self, 'point_color'):
		# 	objs.append( PointSet( vertices, transforms, **kwargs))
		# Only add lines to the graphics objects if one of the line options is
		# specified
		if hasattr(self, 'line_width') or hasattr(self, 'line_style') or hasattr(self, 'line_color'):
			edges = self.gen_edges()
			if hasattr(self, 'edge_colors'):
				for edge, color in zip(edges, self.edge_colors)
					objs.append( LineSet( vertices, [edge], trans=transforms, line_color=color))
			else:
				objs.append( LineSet( vertices, edges, trans=transforms))
		surface_style_options = Surface.trim_style_options(style_options)
		for i in range(6):
			if hasattr(self, 'face_colors'):
				obj.append( Surface( vertices, faces[i:i+2], trans=transforms))
			else:
				obj.append( Surface( vertices, faces[i:i+2], trans=transforms))
		return( RenderableGraphicsObj( *objs, transforms, **style_options))
