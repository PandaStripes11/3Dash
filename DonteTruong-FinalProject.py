# FinalProject.py


from Graphics import *
from time import *
from math import *

from copy import deepcopy 

SCR_WIDTH = 1300
SCR_HEIGHT = 700
beginGrfx(SCR_WIDTH, SCR_HEIGHT) # Viewport dimensions




# region Matrix
class Matrix():
    # Matrices are used for coordinate transformations
    def __init__(self, arr: list = None) -> None:
        """Matrix values are stored in a 2-dimensional list 
        
        Access matrix values with (objName).matrix[row][col].
        If a list isn't specified, the matrix's default values
        are given in row echelon form or a 4D identity matrix:
        [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]]
        """
        if arr is None: # Avoids Python mutating default arguments
            arr = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        self.matrix = arr

    def __mul__(self, matrix: object) -> object:
        """Matrix multiplication
        
        Matrix multiplication is used to accurately
        combine matrix transformations.
        More info:
        https://www.khanacademy.org/math/precalculus/x9e81a4f98389efdf:matrices/x9e81a4f98389efdf:multiplying-matrices-by-matrices/v/multiplying-a-matrix-by-a-matrix
        """
        if len(matrix.matrix) != len(self.matrix[0]):
            print("ERROR::MATRIX::MULTIPLICATION::INVALID_ARGUMENT")
            return
        newMatrix = []
        for row in range(len(self.matrix)):                     # For every row in this matrix
            newRow = []

            matrixRow = self.matrix[row]
            for column in range(len(self.matrix[row])):         # For every colum in this matrix
                matrixCol = []
                for i in range(len(matrix.matrix)):
                    matrixCol.append(matrix.matrix[i][column])
                value = 0
                for j in range(len(matrixRow)):
                    value += matrixRow[j] * matrixCol[j]        # Add up corresponding positions
                newRow.append(value)
            newMatrix.append(newRow)
        return Matrix(newMatrix)

    # Scale Matrix
    def scale(self, x: float, y: float, z: float) -> object:
        """Modifies scale values of matrix

        [[scale.x, 0, 0, 0],
        [0, scale.y, 0, 0],
        [0, 0, scale.z, 0],
        [0, 0, 0, scale.w]]
        """
        scaleValues = [x, y, z, 1]
        newMatrix = Matrix()
        for i in range(len(self.matrix)):
            newMatrix.matrix[i][i] = scaleValues[i]
        self = newMatrix*self
        return self
    # Translation Matrix
    def translate(self, x: float = 0, y: float = 0, z: float = 0) -> object:
        """Modifies translation values of matrix

        [[1, 0, 0, translate.x],
        [0, 1, 0, translate.y],
        [0, 0, 1, translate.z],
        0, 0, 0, 1 (homogenous)]
        """
        transformValues = [x, y, z, 1]
        newMatrix = Matrix()
        for i in range(len(self.matrix)):
            newMatrix.matrix[i][3] = transformValues[i]
        self = newMatrix*self
        return self
    # Rotation Matrix
    def rotate(self, rotationAxis: object, degrees: float) -> object:
        """Rotates coordinate around a vector axis in degrees
        
        General 3D rotation matrix info:
        https://en.wikipedia.org/wiki/Rotation_matrix
        """
        newMatrix = Matrix()
        theta = radians(degrees)
        # Rotate x values
        newMatrix.matrix[0][0] = cos(theta) + (rotationAxis.x ** 2) * (1 - cos(theta))
        newMatrix.matrix[0][1] = rotationAxis.x * rotationAxis.y * (1 - cos(theta)) - rotationAxis.z * sin(theta)
        newMatrix.matrix[0][2] = rotationAxis.x * rotationAxis.z * (1 - cos(theta)) + rotationAxis.y * sin(theta)
        # Rotate y values
        newMatrix.matrix[1][0] = rotationAxis.y * rotationAxis.x * (1 - cos(theta)) + rotationAxis.z * sin(theta)
        newMatrix.matrix[1][1] = cos(theta) + (rotationAxis.y ** 2) * (1 - cos(theta))
        newMatrix.matrix[1][2] = rotationAxis.y * rotationAxis.z * (1 - cos(theta)) - rotationAxis.x * sin(theta)
        # Rotate z values
        newMatrix.matrix[2][0] = rotationAxis.z * rotationAxis.x * (1 - cos(theta)) - rotationAxis.y * sin(theta)
        newMatrix.matrix[2][1] = rotationAxis.z * rotationAxis.y * (1 - cos(theta)) + rotationAxis.x * sin(theta)
        newMatrix.matrix[2][2] = cos(theta) + (rotationAxis.z ** 2) * (1 - cos(theta))
        self = newMatrix*self
        return self

    def perspective(self, aspectRatio: float, fov: float, zNear: float, zFar: float) -> object:
        """Perspective projection

        Generates a perspective matrix using the aspect ratio of the viewport (h/w),
        field of view angle in degrees, zNear (the z value of the plane defining the 
        closest objects that should be visible), and zFar (the z value of the plane 
        defining the farthest objects that should be visible).

        Perspective projection formula intuition info:
        https://www.youtube.com/watch?v=ih20l3pJoeU&t=1697s
        """
        fov = radians(fov)
        perspective = [
            [aspectRatio * (1/tan(fov)), 0, 0, 0],
            [0, (1/tan(fov)), 0, 0],
            [0, 0, (zFar/(zFar - zNear)), 1],
            [0, 0, (-zFar * zNear)/(zFar - zNear), 0]
        ]
        perspectiveMatrix = Matrix(perspective)
        self = perspectiveMatrix * self
        return self
# endregion




# region Vector
class Vector():
    def __init__(self, x: float, y: float, z: float) -> None:
        """Vector values are stored in array/list and variables

        Access the list values use objName.arr.
        Use .x, .y, or .z to access single variables.
        """
        self.x = x
        self.y = y
        self.z = z
        self.w = 1

        self.arr = [x, y, z, self.w]

    def __mul__(self, matrix: list) -> object:
        """Vector * matrix
        
        Make sure matrix is given as a
        2D list and NOT as a matrix obj.
        """
        # Update list values
        newVector = []
        for row in range(len(self.arr)):                        # For every component of the vector/matrix
            val = 0
            for column in range(len(matrix[row])):            # For every value in the vector/matrix row
                val += matrix[row][column] * self.arr[column] # Multiply the corresponding matrix value and add
            newVector.append(val)
        self.arr = newVector
        # Perspective division - divides vector by w component
        self.w = self.arr[3]
        for i in range(len(self.arr)):
            self.arr[i] = self.arr[i] / self.w
        # Update variable values
        self.x = self.arr[0]
        self.y = self.arr[1]
        self.z = self.arr[2]
        self.w = self.arr[3]
        return self
    def normalize(self) -> float:
        """Normalization function
        
        Makes the magnitude of the vector 1.
        Unit vector is calculated by dividing
        each component of the vector by the
        length.
        """
        length = sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2) # Calculates length of vector (Pythagorean Theorem)
        if length == 0:
            return 0
        # Divide components by length
        self.arr[0] = self.x / length
        self.arr[1] = self.y / length
        self.arr[2] = self.z / length
        
        # Update list values
        self.x = self.arr[0]
        self.y = self.arr[1]
        self.z = self.arr[2]
        return length
# endregion




# region Polygon
class Polygon():
    def __init__(self, coordinates: list, model: object = None) -> None:
        """2D Polygons in 3D Space
        
        Uses model matrix to draw coordinates
        in world (3D) space.
        local coordinates * model matrix = world space coordinates
        """
        self.coordinates = coordinates
        
        if model is None: # Avoids Python mutating default model argument
            model = Matrix()
        self.model = model
    
    def transform_to_view_space(self, model: list) -> list:   
        """Transforms all coordinates into view space (camera)
        
        The coordinates of the square go from local
        space -> world space -> view space (camera view)
        """
        if model is None:
            model = self.model
        # Creates a new variable assigned only to the value of self.coordinates (not a reference)     
        coordinatesCopy = deepcopy(self.coordinates)

        viewSpaceCoordinates = []
        for i in range(len(self.coordinates)):  # For each coordinate
            viewSpaceCoordinates.append(((      # Transform to view space
                self.coordinates[i] *       # local space
                model.matrix) *             # world space
                view.matrix)                # view space
            )
        self.coordinates = coordinatesCopy # resets coordinates back to original

        return viewSpaceCoordinates
    def transform_to_screen_space(self) -> list:   
        """Transforms all coordinates into screen space
        
        The coordinates of the square go from local
        space -> world space -> view space -> clip
        space -> screen space
        """
        # Creates a new variable assigned only to the value of self.coordinates (not a reference)     
        coordinatesCopy = deepcopy(self.coordinates)

        screenSpaceCoordinates = []
        for i in range(len(self.coordinates)):  # For each coordinate
            screenSpaceCoordinates.append((((   # Transform to screen space
                self.coordinates[i] *       # local space
                self.model.matrix) *        # world space
                view.matrix) *              # view space
                projection.matrix) *        # clip space
                viewportTransform.matrix    # screen space
            )
        self.coordinates = coordinatesCopy # resets coordinates back to original

        return screenSpaceCoordinates
    def draw(self, model: object = None) -> list:
        """Drawing in 2D Traditional Graphics
        
        Formats the screen space coordinates into
        a traditional graphics's fillPolygon argument
        list. Then, it is a simple matter of calling
        fillPolygon with the new list and outlining it
        with black using drawPolygon.
        """
        if model is None:
            model = Matrix()
        self.model = model

        screenSpaceCoordinates = self.transform_to_screen_space()   # Gets screen space coordinates
        traditionalGraphicsCoordinates = []
        for i in range(len(self.coordinates)):                                  # For each coordinate
            traditionalGraphicsCoordinates.append(screenSpaceCoordinates[i].x)  # Add the x coordinate
            traditionalGraphicsCoordinates.append(screenSpaceCoordinates[i].y)  # Add the y value
        
        # Render the polygon
        fillPolygon(traditionalGraphicsCoordinates)
        # Outline the polygon
        setColor("black")
        drawPolygon(traditionalGraphicsCoordinates)
        return traditionalGraphicsCoordinates
# endregion




# region Square
class Square(Polygon):
    def __init__(self, model: list = None):
        """Square coordinates
        
        Inherits from the Polygon class
        using local coordinates for a square.
        """
        coordinates = [
            Vector(-1, -1, 0),  # Bottom left
            Vector(1, -1, 0),   # Bottom right
            Vector(1, 1, 0),    # Top right
            Vector(-1, 1, 0)    # Top left
        ]
        super().__init__(coordinates, model)
# endregion




# region Triangle
class Triangle():
    def __init__(self, model: list = None):
        """Triangle coordiantes
        
        Inherits from the Polygon class
        with coordinates for a triangle
        inscribed in a 2x2 square.
        """
        coordinates = [
            Vector(-1, -1, 0),  # Bottom right
            Vector(1, -1, 0),   # Bottom left
            Vector(0, 1, 0)     # Top
        ]
        super().__init__(coordinates, model)
# endregion




# region Polyhedron
class Polyhedron():
    def __init__(self, coordinates: list, faces: list, model: object = None, color = None):
        """3D Shapes
        
        Takes a list of vertex coordinates, faces, and a model
        transformation matrix. Faces are a list of coordinate indices
        specifying the order of coordinates for a polygon. These polygons
        are stored in a list and transformed into world space using the
        model matrix.
        """
        self.coordinates = coordinates
        self.faces = faces
        if model is None:       # Defaults to identity model matrix
            model = Matrix()
        self.model = model

        if color is None:       # Defaults to gray color
            color = "gray"
        self.color = color      #TODO: ADD COMPATIBILITY FOR RGB COLORS

        self.polygons = []
        for face in faces:                                              # For each face
            faceCoords = []
            for index in face:                                          # For each index in face
                faceCoords.append(deepcopy(self.coordinates[index]))    # Append the corresponding coordinate
            self.polygons.append(Polygon(faceCoords))                   # Append Polygon using ordered coordinates
        
        self.polygonDepths = [] # holds Z values of each polygon
        self.zValue = None      # holds the average Z value of entire shape
    
    def draw(self, model: object = None):
        """Renders 3D shape
        
        Sorts the polygons from back to front and draws
        in that order.
        """
        if model is None:
            model = self.model

        self.depth_sort(self.polygons, model)           # sorts polygons from back to front
        for index, polygon in enumerate(self.polygons): # for each polygon
            if type(self.color) == str:
                setColor(self.color)
            elif type(self.color) == list:
                setColor(self.color[0], self.color[1], self.color[2])                        
            polygon.draw(model)                         # call the polygon's draw method
    def depth_sort(self, polygons: list, model: list = None) -> list:
        """Sorts polygons from back to front (-Z to Z values)"""
        # Sort z values
        zValues = []
        for index, polygon in enumerate(polygons):                          # for reach polygon
            val = 0
            viewSpaceCoordinates = polygon.transform_to_view_space(model)   # transform to view space
            for vertex in viewSpaceCoordinates:                             
                val += vertex.z                                             # add up the vertices' z values
            zValues.append((index, val/len(polygon.coordinates)))           # append the index and average of the z values
        zValues.sort(key=lambda zValue: zValue[1])                          # sort the zValues list
        
        # Sort polygons using corresponding zValues
        newPolygons = []
        polygonDepths = []
        for zValue in zValues:                                              # for each zValue
            polygonDepths.append(zValue[1])                                 # append the zValue
            newPolygons.append(self.polygons[zValue[0]])                    # add to the new list the corresponding polygon index
        self.polygons = newPolygons
        self.polygonDepths = polygonDepths
        self.zValue = sum(polygonDepths)/len(zValues)                       # calculate average depth of entire polyhedron
        return self.polygons
# endregion




# region Cube
class Cube(Polyhedron):
    def __init__(self, model: object = None, color: str = None):
        """Creates polyhedron using coordinates for a cube"""
        coordinates = [
            # Front face
            Vector(-1, -1, 1),  # Bottom left
            Vector(1, -1, 1),   # Bottom right
            Vector(1, 1, 1),    # Top right
            Vector(-1, 1, 1),   # Top left

            # Back face
            Vector(-1, -1, -1),
            Vector(1, -1, -1),
            Vector(1, 1, -1),
            Vector(-1, 1, -1),
        ]
        faces = [
            [0, 1, 2, 3], # Front face
            [4, 5, 6, 7], # Back face
            [2, 1, 5, 6], # Right face
            [3, 0, 4, 7], # Left face
            [2, 3, 7, 6], # Top face
            [0, 1, 5, 4], # Bottom face
        ]
        super().__init__(coordinates, faces, model, color)
# endregion




# region Tetrahedron
class Tetrahedron(Polyhedron):
    def __init__(self, model: object = None, color: str = None):
        """Creates polyhedron using coordinates for a tetrahedron
        
        Exact coordinate values were calculated beforehand.
        """
        coordinates = [
            # Base
            Vector(-1, -0.40825, -1.062,),
            Vector(1, -0.40825, -1.062,),
            Vector(0, -0.40825, 1.062),

            # Tip
            Vector(0, 1.2247, 0)
        ]
        faces = [
            [0, 1, 2],
            [0, 1, 3],
            [1, 2, 3],
            [0, 2, 3]
        ]
        super().__init__(coordinates, faces, model, color)
# endregion




# region Coordinate Space Matrices
""" MATRICES """
# View matrix (View space = camera view; transforms world coordinates to position of the "camera")
view = Matrix()
view = view.translate(6,18,-10)
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




# region Scene
class Scene():
    def __init__(self, polyhedrons: dict = None):
        """Scene object
        
        Stores all current polyhedrons, sorts by z-order,
        and draws.
        """
        if polyhedrons is None:
            polyhedrons = {}
        self.polyhedrons = polyhedrons
        self.polyhedronsList = list(self.polyhedrons.values())

    def add_polyhedron(self, name: str, polyhedron: object):
        self.polyhedrons[name] = polyhedron
        self.polyhedronsList = list(self.polyhedrons.values())

    def draw(self):
        self.depth_sort()
        for polyhedron in self.polyhedronsList:
            polyhedron.draw()
    def depth_sort(self):
        #TODO: FIX DEPTH BUFFER TO DRAW BY INDIVIDUAL POLYGON ORDER
        zValues = []
        for index, polyhedron in enumerate(self.polyhedronsList):
            polyhedron.depth_sort(polyhedron.polygons, polyhedron.model)
            zValues.append((index, polyhedron.zValue))
        zValues.sort(key=lambda zValue: zValue[1])

        newPolyhedrons = []
        for zValue in zValues:
            newPolyhedrons.append(deepcopy(self.polyhedronsList[zValue[0]]))
        self.polyhedronsList = newPolyhedrons
# endregion




# region Camera
"""Event listener functions

Reads input and modifies view matrix accordingly.
"""
listen()
class KeyState:
    def __init__(self, key):
        self.key = key
        self.down = False
        onkeypress(self.press, key)
        onkeyrelease(self.release, key)

    def press(self):
        self.down = True

    def release(self):
        self.down = False
w_key = KeyState('w')
a_key = KeyState('a')
s_key = KeyState('s')
d_key = KeyState('d')
space_key = KeyState('space')
shift_key = KeyState('Shift_L')

up_arrow = KeyState('Up')
left_arrow = KeyState('Left')
down_arrow = KeyState('Down')
right_arrow = KeyState('Right')

def processInput():
    global view

    if w_key.down:
        view = view.translate(0, 0, 0.1)
    if a_key.down:
        view = view.translate(-cubeVelocity.z/120, 0, -cubeVelocity.z/120)
    if s_key.down:
        view = view.translate(0, 0, -0.1)
    if d_key.down:
        view = view.translate(-0.1, 0, 0)

    if space_key.down:
        #view = view.translate(0, -0.1, 0)
        if cubeVelocity.y == 0: cubeVelocity.y = 20
    if shift_key.down:
        view = view.translate(0, 0.1, 0)

    if up_arrow.down:
        view = view.rotate(Vector(1, 0, 0), -1)
    if down_arrow.down:
        view = view.rotate(Vector(1, 0, 0), 1)
    if right_arrow.down:
        view = view.rotate(Vector(0, 1, 0), 1)
    if left_arrow.down:
        view = view.rotate(Vector(0, 1, 0), -1)
# endregion




class GameObject():
    pass




cubePos = Vector(0,0,0)
cubeVelocity = Vector(0,0,-5)




"""INITIALIZE SCENE"""
scene = Scene()
def init():
    global scene

init()
"""INITIALIZE SCENE"""


# TODO: Change polyhedron model matrix to transform values
# TODO: Create Game State
# TODO: Create UI classes

""" RENDER LOOP """
def render(scene: object):
    global view

    currFrame = None; prevFrame = time(); deltaTime = None

    global cubeVelocity
    global cubePos
    groundHeight = -20
    while 0 == 0:
        currFrame = time()
        deltaTime = currFrame - prevFrame
        prevFrame = time()

        processInput()

        # Player
        model = Matrix()
        if cubePos.y >= groundHeight:
           cubeVelocity.y -= 4*9.87*deltaTime
           cubePos.y += cubeVelocity.y*deltaTime
        elif not cubeVelocity.y > 0:
            cubeVelocity.y = 0
        deltaX = cubeVelocity.x*deltaTime; deltaY = cubeVelocity.y*deltaTime; deltaZ = cubeVelocity.z*deltaTime
        cubePos.x += deltaX
        cubePos.y += deltaY
        cubePos.z += deltaZ

        model = model.rotate(Vector(1,0,0), cubeVelocity.z*deltaTime)
        model = model.translate(cubePos.x,cubePos.y,cubePos.z)

        viewVector = Vector(-deltaZ*0.7071, 0, -deltaZ*0.7071)
        print(viewVector.arr, [deltaX, deltaY, deltaZ])
        view = view.translate(viewVector.x, viewVector.y, viewVector.z)

        scene.add_polyhedron("player", Cube(model, "gold"))

        # Update buffers
        clear()
        scene.draw()
        update()
render(scene)
""" RENDER LOOP """




endGrfx()
