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
		self.trans_mat = Mat34(1,0,0,0,0,1,0,0,0,0,1,0)
		for t in self.transforms:
			self.trans_mat = t.get_mat(self)*self.trans_mat
		for key in kwargs.keys():
			if key in self.graphics_properties:
				self.validate_style_options(key, kwargs[key])
				setattr(self,key,kwargs[key])
			else:
				name = self.__class__.__name__
				raise AttributeError("{}.__init__ keyword options must be valid style options".format(name))

	def calc_center( self, display_radius=None):
		cms = [obj.calc_center( display_radius) for obj in self.obj_list]
		areas = [obj.calc_area( display_radius) for obj in self.ojb_list]
		num = sum( [cm*area for cm, area in zip(cms, areas)])
		denom = sum( areas)
		return( self.trans_mat*(num/denom))		

	def calc_area( self, display_radius=None):
		areas = [obj.calca_area( display_radius) for obj in self.ojb_list]
		return( sum( areas))	

	def validate_style_options(self, option_name, option_value):
		if option_name.split('_')[-1] == 'color':
			if not isinstance(option_value, RGBA):
				raise ValueError("Color options must be valid color objects")
		elif options_name.split('_') == 'colors'
			if options_name == 'face_colors' and len(option_value) != len(self.faces):
				raise AttributeError("Face colors must be a sequence of colors the same length as the list of faces")
			if options_name == 'edge_colors' and len(option_value) != len(self.edges):
				raise AttributeError("Edge colors must be a sequence of colors the same length as the list of edges")
			if options_name == 'vertex_colors' and len(option_value) != len(self.edges):
				raise AttributeError("Vertex colors must be a sequence of colors the same length as the list of vertices")
			for item in option_value:
				if not isinstance(option_value, RGBA):
					raise ValueError("Color options must be valid color objects")
		elif option_name == 'specularity':
			if not isinstance(option_value, number.Numbers):
				raise ValueError("Specularity must be a number")
		elif option_name == 'line_width':
			if not isinstance(option_value, number.Numbers) or not( 1. < line_width < 10.):
				raise ValueError("Line width must be a number between 1 and 10")
		elif option_name == 'point_size':
			if not isinstance(option_name, number.Numbers) or not( 1. < point_size < 30):
				raise ValueError("Point size must be a number between 1 and 30")
		elif option_name == 'line_style':
			if option_value not in lineStyleSet:
				raise ValueError("Line style is 'solid', 'dashed' or 'dotted'")
		elif option_name == 'point_style':
			if option_value not in pointStyleSet:
				raise ValueError("Point Style must be a valid point style")

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

	graphics_options = ['color',
						'specular_color',
						'specularity',
						'line_color',
						'line_width',
						'line_style',
						'point_color',
						'point_size',
						'point_style']

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
