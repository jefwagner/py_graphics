# Author: Jef Wagner
# Date: 13-02-2015

class BaseGraphicsObj:

	def __init__(self, trans=[], **kwargs):
		self.transforms = []
		for t in trans:
			if isinstance( t, Transform):
				self.transforms.append(t)
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__init__ transform options must be an sequence of Transforms".format(name))
		self.trans_mat = Mat34(np.eye(3))
		for t in self.transforms:
			self.trans_mat = t.get_mat(self)*self.trans_mat
		for key in kwargs.keys():
			if key in self.graphics_properties:
				setattr(self,key,kwargs[key])
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__init__ keyword options must be valid style options")

	def center_of_mass( self, display_radius=None):
		cms = [obj.center_of_mass( display_radius) for obj in self.obj_list]
		areas = [obj.areas( display_radius) for obj in self.ojb_list]
		num = sum( [cm*area for cm, area in zip(cms, areas)])
		denom = sum( areas)
		return( self.trans_mat*(num/denom))		

	def area( self, display_radius=None):
		areas = [obj.areas( display_radius) for obj in self.ojb_list]
		return( sum( areas))	

	def get_style_options(self):
		style_options={}
		for opt in self.graphics_properties:
			if hasattr(self, opt):
				style_options[opt] = getattr(self, opt)
		return( style_options)

	@classmethod
	def trim_style_options(cls, **kwargs):
		style_options={}
		for opt in kwargs:
			if opt in cls.style_options:
				style_options[opt] = kwargs[opt]
		return( style_options)

class GraphicsObj(BaseGraphicsObj):

	def __init__( self, *args, transforms=[], **kwargs):
		for obj in args:
			if isinstance(BaseGraphicsObj, obj):
				self.obj_list.append(obj)
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__init__ takes and array of BaseGraphicsObjs")
		super(GraphicsObjs, self).__init__(transforms, **kwargs)

	def to_renderable(self, display_radius=None):
		rend_obj_list = [obj.to_renderable() for obj in self.obj_list]
		style_options = self.get_style_options()
		return( RenderableGraphicsObj(rend_obj_list, trans=self.transforms, **style_options))


class RenderableGraphicsObj(BaseGraphicsObj):

	def __init__( self, *args, transforms=[], **kwargs):
		for obj in args:
			if isinstance(RenderableGraphicsObj, obj):
				self.obj_list.append(obj)
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__init__ takes and array of RenderableGraphicsObjs")
		super(RenderableGraphicsObjs, self).__init__(transforms, **kwargs)

	def to_renderable(self, display_radius=None):
		return( self)