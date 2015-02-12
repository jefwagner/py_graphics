# Author: Jef Wagner
# Date: 10-02-2015

class Edge(IVec2):

	def pts(self, vertices, trans_mat):
		pt0 = trans_mat*vertices[self[0]]
		pt1 = trans_mat*vertices[self[1]]
		return( pt0, pt1)

	def center_of_mass(self, vertices, trans_mat):
		pt0, pt1 = self.pts( vertices, trans_mat)
		return( (pt0+pt1)/2)

	def length( self, vertices, trans_mat):
		pt0, pt1 = self.pts( vertices, trans_mat)
		return( (pt0-pt1).mag())

class Face(IVec3):

	def pts(self, vertices, trans_mat)):
		pt0 = trans_mat*vertices[self[0]]
		pt1 = trans_mat*vertices[self[1]]
		pt2 = trans_mat*vertices[self[2]]
		return( pt0, pt1, pt2)		

	def center_of_mass(self, vertices, trans_mat):
		pt0, pt1, pt2 = self.pts( vertices, trans_mat)
		return( (pt0+pt1+pt2)/3.)

	def area(self, vertices, trans_mat):
		pt0, pt1, pt2 = self.pts( vertices, trans_mat)
		n = pt0.cross(pt1) + pt1.cross(pt2) + pt2.cross(pt0)
		return( 0.5*n.mag())

	def normal(self, vertices, trans_mat):
		pt0, pt1, pt2 = self.pts( vertices, trans_mat)
		n = pt0.cross(pt1) + pt1.cross(pt2) + pt2.cross(pt0)
		return( n.unit())

class Surface(RenderableGraphicsObj):

	graphics_options = ['color',
						'ambient_color',
						'specular_color',
						'specularity',
						'vertex_colors']

	def __init__(self, vertices, faces, transforms=[], **kwargs):
		self.vertices = []
		for v in vertices:
			self.vertices.append( Vec3(v))
		self.faces = []
		for f in faces:
			self.faces.append( Face(f))
		super(Surface, self).__init__(transforms, **kwargs)

	def gen_face_areas():
		if not hasattr(self, 'face_areas'):
			self.face_areas = [f.area(self.vertices, self.trans_mat) for f in self.faces]
		return( self.face_areas)

	def gen_face_center_of_masses():
		if not hasattr(self, 'face_center_of_masses'):
			self.face_center_of_masses = [f.center_of_mass(self.vertices, self.trans_mat) for f in self.faces]
		return( self.face_center_of_masses)

	def gen_face_normals(self):
		if not hasattr(self, 'face_normals'):
			self.face_normals = [f.normal(self.vertices, self.trans_mat) for f in self.faces]
		return( self.face_normals)

	def gen_vertex_normals(self):
		if not hasattr(self, 'vertex_normals'):
			vns = [None]*len(self.vertices)
			w = [None]*len(self.vertices)
			fns = self.gen_face_normals()
			areas = self.gen_face_areas()
			for (f, fn, a) in zip(self.faces, fns, areas):
				for index in f:
					if vns[index] == None:
						vns[i] = fn
						w[i] = a
					else:
						vns[i] = (w*vns[i]+a*fn)/(w[i]+a)
						w[i] = w[i]+a
			self.vertex_normals = vns
		return( self.vertex_normals)

	def center_of_mass(self, display_radius=None):
		cms = self.gen_face_center_of_masses()
		areas = self.gen_face_areas()
		num = sum( [cm*area for cm, area in zip(cms, areas)])
		denom = sum( areas)
		return( self.trans_mat*(num/denom))

	def area(self, display_radius=None):
		areas = self.gen_face_areas()
		return( sum(areas))


class LineSet(RenderableGraphicsObj):

	graphics_options = ['line_color',
						'line_width',
						'line_style',
						'vertex_colors']

	def __init__(self, vertices, edges, transforms=[], **kwargs):
		self.vertices = []
		for v in vertices:
			self.vertices.append( Vec3(v))
		self.edges = []
		for e in edges:
			self.edges.append( Edge(e))
		super(LineSet, self).__init__(transforms, **kwargs)

	def gen_edge_lengths(self):
		if not hasattr(self, 'edge_lengths'):
			self.edge_lengths = [e.length(self.vertices, self.trans_mat) for e in self.edges]
		return( self.edge_lengths)

	def gen_edge_center_of_masses(self):
		if not hasattr(self, 'edge_center_of_masses')
			self.edge_center_of_masses = [e.center_of_mass(self.vertices, self.trans_mat) for e in self.edges]
		return( self.edge_lengths)

	def center_of_mass(self, display_radius = None):
		csm = self.gen_edge_center_of_masses()
		lengths = self.gen_line_lengths()
		num = sum( [cm*l for cm, l in zip(cms, lengths)])
		denom = sum( [l for l in lengths])
		return( num/denom)

	def area(self, display_radius = None):
		dx = calc_dx_from_line_width( self.line_width, display_radius)
		return( dx*sum( self.gen_line_lengths))

class Line(LineSet):

	def __init__(self, vertices, closed=False, transforms=[], **kwargs):
		n = len(vertices)-1
		self.edges = [ Edge(i,i+1) for i in range(n)]
		if closed:
			self.edges.append( Edge(n,0))
		super(Line, self).__init__(transforms, **kwargs)

class Billboard(RenderableGraphicsObj)

	def __init__(self, vertex, size, transforms=[], **kwargs):
		self.size = Vec2( size)
		self.vertex = Vec3(vertex):
		super(Billboard, self).__init__(transforms, **kwargs)
