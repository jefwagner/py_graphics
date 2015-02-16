PyGraphics: Another Python based graphics system
================================================

I want to create a graphics system similar to Mathematica's.

+ There are three basic types of basic renderable objects
    - Surface
    - LineSet
    - Billboards

+ We can combine these items into combined renderable object
    - RenderableGraphicsObj

+ There are basic geometric objects that can be constructed from 
  these
    - Spheres
    - Cylinder
    - Cone
    - Box
    - Pyramid
    - Tetrahedron
    - Disk
    - Polygon
    - Line
    - Spline
    - Point

+ There are complicated constructed geometric shapes
    - Extrusion

+ We can combine these to a combined graphics object
    - GraphicsObj

+ We can specify style properties with keyword objects
    - color
    - ambient_color
    - specular_color
    - specularity
    - line_color
    - line_width
    - line_style
    - point_color
    - point_size
    - point_style
    - face_colors
    - edge_colors
    - vertex_colors

+ There are basic transformation that can be specified for each
  graphics object
    - Translate
    - Scale
    - Shear
    - Rotate

+ There should be basic light objects
    - Ambient light
    - Directional light
    - Point light
    - Spot light

+ We can combine these to a combined light object
    - LightObj

+ There should be a camera object
    - Camera

+ I would like to have a render call that takes a graphics object, a 
  lighting object, and a camera object to render a scene.
    - Default to creating a WebGL scene
    - Render directly to picture (png, jpg, svg)
