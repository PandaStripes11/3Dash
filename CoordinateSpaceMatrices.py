from Math import *

SCR_WIDTH = 1300
SCR_HEIGHT = 700

# region Coordinate Space Matrices
""" MATRICES """
# View matrix (View space = camera view; transforms world coordinates to position of the "camera")
view = Matrix()
view = view.translate(15,14,-15)
view = view.rotate(Vector(0,1,0),45)

# Perspective projection matrix (Clip space = projects 3D coordinates to 2D range from -1.0 to 1.0)
projection = Matrix()
projection = projection.perspective(SCR_HEIGHT/SCR_WIDTH, 70.0, 0.2, 100.0)

# Viewport transform (Screen space = stretches out 2D coordinates to fit 1300x700 viewport)
viewportTransform = Matrix()
viewportTransform = viewportTransform.scale(SCR_WIDTH/2, -SCR_HEIGHT/2, 1)
viewportTransform = viewportTransform.translate(SCR_WIDTH/2, SCR_HEIGHT/2, 0)
""" MATRICES """
# endregion