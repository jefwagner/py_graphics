# Author: Jef Wagner
# Date: 14-02-2015

class Billboard(RenderableGraphicsObj)

  def __init__(self, vertex, size, texture_id, transforms=[], **kwargs):
    self.size = Vec2( size)
    self.vertex = Vec3(vertex):
    self.texture_id = texture_id
    super(Billboard, self).__init__(transforms, **kwargs)
