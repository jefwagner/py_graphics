# Author: Jef Wagner
# Date: 14-02-2015


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
