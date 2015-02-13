PyGraphics: Another Python based graphics system
================================================

I want to create a graphics system similar to Mathematica's. 
+ I would like to have a set of graphics primitives.
    - Points
    - Text
    - Lines
    - Polygon
    - Circle
    - Box
    - Sphere
    - Cylinder
    - Cone
+ The primitives can combined together into more complicated graphics objects. 
+ I would like properties such as color, opacity, specularity, etcetera to be named parameters of each graphics object. 
+ I would like all graphics objects to have several methods associated with them
    - Center of mass
    - Bounding box
    - Bounding sphere
+ I would like to have several transformation's
    - Scale
    - Shear
    - Rotate
    - Translate
+ I would like to have a lighting objects
    - Directional lights
    - Point lights
    - Spot lights
    - Combined lighting 
    - Several default lighting signatures
        * Tri-color
        * Neutral
+ I would like to have camera objects
    - Perspective camera
    - Orthographic camera
+ I would like to have a render call that takes a graphics object, a lighting object, and a camera object to render a scene.
    - Default to creating a WebGL scene using three.js buffer geometry
    - Render directly to picture
+ In addition I would like to create 2-D scenes using an orthographic camera