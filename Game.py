# FinalProject.py


from Graphics import *
from time import *
from copy import deepcopy

from Math import *
from CoordinateSpaceMatrices import *
from Scene import Scene


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




# region Inputs
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
e_key = KeyState('e')
space_key = KeyState('space')
shift_key = KeyState('Shift_L')

up_arrow = KeyState('Up')
left_arrow = KeyState('Left')
down_arrow = KeyState('Down')
right_arrow = KeyState('Right')

def processInput():
    global gameObjects
    global w_key, a_key, s_key, d_key, e_key, space_key, shift_key
    global view
    if w_key.down:
        #view = view.translate(0, 0, 0.1)
        gameObjects[0].velocity.z = -20
    if a_key.down:
        #view = view.translate(0.1, 0, 0)
        gameObjects[0].velocity.x = -10
    if s_key.down:
        #view = view.translate(0, 0, -0.1)
        gameObjects[0].velocity.z= -10
    if d_key.down:
        #view = view.translate(-0.1, 0, 0)
        gameObjects[0].velocity.x = 10
    if not a_key.down and not d_key.down:
        gameObjects[0].velocity.x = 0
    if not s_key.down and not w_key.down:
        gameObjects[0].velocity.z = -15

    if space_key.down:
        #view = view.translate(0, -0.1, 0)
        if gameObjects[0].velocity.y == 0: gameObjects[0].velocity.y = 40
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




# region GameObject
class GameObject():
    def __init__(
        self, 
        name: str,
        shape: Polyhedron,
        translate: Vector = Vector(0,0,0), 
        rotate: list = [Vector(1,0,0), 0], 
        scale: Vector = Vector(1,1,1)
    ):
        self.name = name
        self.shape = shape
        self.transform = {
            "translate": translate,
            "rotate": rotate,
            "scale": scale
        }
        self.viewPos = 15

    def add(self):
        model = Matrix()
        model = model.scale(                    # Scale
            self.transform["scale"].x,
            self.transform["scale"].y,
            self.transform["scale"].z
        )
        if self.transform["rotate"][1] != 0:    # Rotate
            model = model.rotate(self.transform["rotate"][0].normalize(), self.transform["rotate"][1])
        model = model.translate(                # Translate
            self.transform["translate"].x,
            self.transform["translate"].y,
            self.transform["translate"].z
        )

        global scene
        self.shape.model = model
        scene.add_polyhedron(self.name, self.shape)
    def update(self, deltaTime = None):
        self.viewPos += -15*deltaTime
        if self.transform["translate"].z >= self.viewPos:
            scene.remove_polyhedron(self.name)
            self.viewPos = 15
# endregion




# region Obstacle
class Obstacle(GameObject):
    def __init__(self, name: str, translate: Vector = Vector(0, 0, 0), rotate: list = [Vector(1, 0, 0), 0], scale: Vector = Vector(1, 1, 1)):
        super().__init__(name, Cube(), translate, rotate, scale)
    def _inside(self):
        obstaclePos = self.transform["translate"]
        obstacleScale = self.transform["scale"]
        obstacleMin = Vector(obstaclePos.x - 1*obstacleScale.x, obstaclePos.y - 1*obstacleScale.y, obstaclePos.z - 1*obstacleScale.z)
        obstacleMax = Vector(obstaclePos.x + 1*obstacleScale.x, obstaclePos.y + 1*obstacleScale.y, obstaclePos.z + 1*obstacleScale.z)

        playerPos = gameObjects[0].transform["translate"]
        cubeMin = Vector(playerPos.x-1, playerPos.y-1, playerPos.z-1)
        cubeMax = Vector(playerPos.x+1, playerPos.y+1, playerPos.z+1)
        
        return (
            (obstacleMin.x < cubeMax.x and obstacleMax.x > cubeMin.x) and
            (obstacleMin.y < cubeMax.y and obstacleMax.y > cubeMin.y) and
            (obstacleMin.z < cubeMax.z and obstacleMax.z > cubeMin.z)
        )
    def update(self, deltaTime = None):
        global scene
        
        super().update(deltaTime)

        playerPos = gameObjects[0].transform["translate"]
        playerVelocity = gameObjects[0].velocity

        isInside = self._inside()
        if isInside and playerPos.z >= self.transform["translate"].z+self.transform["scale"].z-1:
            playerVelocity.z = 0
            playerPos.z = self.transform["translate"].z + self.transform["scale"].z + 1
        elif isInside and playerVelocity.y < 0:
            playerVelocity.y = 0
            playerPos.y = self.transform["translate"].y + self.transform["scale"].y + 1
        elif isInside and playerVelocity.y > 0:
            playerVelocity.y = 0
            playerPos.y = self.transform["translate"].y - self.transform["scale"].y - 1
        elif isInside and playerPos.z <= self.transform["translate"].z+self.transform["scale"].z+1 and playerVelocity.x != 0:
            if playerVelocity.x > 0: playerPos.x = self.transform["translate"].x - self.transform["scale"].x - 1
            else: playerPos.x = self.transform["translate"].x + self.transform["scale"].x + 1
            playerVelocity.x = 0
        gameObjects[0].add()
# endregion




# region Spike
class Spike(GameObject):
    def __init__(self, name: str, translate: Vector = Vector(0, 0, 0), rotate: list = [Vector(1, 0, 0), 0], scale: Vector = Vector(1, 1, 1)):
        super().__init__(name, Tetrahedron(color="red"), translate, rotate, scale)
    def _inside(self):
        obstaclePos = self.transform["translate"]
        obstacleScale = self.transform["scale"]
        obstacleMin = Vector(obstaclePos.x - 1*obstacleScale.x, obstaclePos.y - 1*obstacleScale.y, obstaclePos.z - 1*obstacleScale.z)
        obstacleMax = Vector(obstaclePos.x + 1*obstacleScale.x, obstaclePos.y + 1*obstacleScale.y, obstaclePos.z + 1*obstacleScale.z)

        
        playerPos = gameObjects[0].transform["translate"]
        cubeMin = Vector(playerPos.x-1, playerPos.y-1, playerPos.z-1)
        cubeMax = Vector(playerPos.x+1, playerPos.y+1, playerPos.z+1)
        
        return (
            (obstacleMin.x < cubeMax.x and obstacleMax.x > cubeMin.x) and
            (obstacleMin.y < cubeMax.y and obstacleMax.y > cubeMin.y) and
            (obstacleMin.z < cubeMax.z and obstacleMax.z > cubeMin.z)
        )
    def update(self, deltaTime = None):
        super().update(deltaTime)

        playerPos = gameObjects[0].transform["translate"]
        playerVelocity = gameObjects[0].velocity
        if self._inside():
            playerPos.x = 0; playerPos.y = 0; playerPos.z = 0
            playerVelocity.x = 0; playerVelocity.y = 0; playerVelocity.z = 0

            gameObjects[0].kill()
# endregion




# region Finish
class Finish(GameObject):
    def __init__(self, name: str, translate: Vector = Vector(0, 0, 0), rotate: list = [Vector(1, 0, 0), 0], scale: Vector = Vector(1, 1, 1)):
        super().__init__(name, Cube(color="white"), translate, rotate, scale)
        self.finished = False
    def _inside(self):
        obstaclePos = self.transform["translate"]
        obstacleScale = self.transform["scale"]
        obstacleMin = Vector(obstaclePos.x - 1*obstacleScale.x, obstaclePos.y - 1*obstacleScale.y, obstaclePos.z - 1*obstacleScale.z)
        obstacleMax = Vector(obstaclePos.x + 1*obstacleScale.x, obstaclePos.y + 1*obstacleScale.y, obstaclePos.z + 1*obstacleScale.z)

        playerPos = gameObjects[0].transform["translate"]
        cubeMin = Vector(playerPos.x-1, playerPos.y-1, playerPos.z-1)
        cubeMax = Vector(playerPos.x+1, playerPos.y+1, playerPos.z+1)
        
        return (
            (obstacleMin.x < cubeMax.x and obstacleMax.x > cubeMin.x) and
            (obstacleMin.y < cubeMax.y and obstacleMax.y > cubeMin.y) and
            (obstacleMin.z < cubeMax.z and obstacleMax.z > cubeMin.z)
        )
    def update(self, deltaTime = None):
        super().update(deltaTime)

        if self._inside() or self.finished:
            self.finished = True
            gameObjects[0].finish()

        isInside = self._inside()
        playerPos = gameObjects[0].transform["translate"]
        playerVelocity = gameObjects[0].velocity
        if isInside and playerPos.z >= self.transform["translate"].z+1:
            playerVelocity.z = 0
            playerPos.z = self.transform["translate"].z + 2
        elif isInside and playerVelocity.y < 0:
            playerVelocity.y = 0
            playerPos.y = self.transform["translate"].y + self.transform["scale"].y + 1
        elif isInside and playerPos.z <= self.transform["translate"].z+2 and playerVelocity.x != 0:
            if playerVelocity.x > 0: playerPos.x = self.transform["translate"].x - 2
            else: playerPos.x = self.transform["translate"].x + 2
            playerVelocity.x = 0
# endregion




# region Player
class Player(GameObject):
    def __init__(self, 
        name: str, 
        translate: Vector = Vector(0, 0, 0), 
        rotate: list = [Vector(1, 0, 0), 0], 
        scale: Vector = Vector(1, 1, 1),
        velocity: Vector = Vector(0, 0, 0)
    ):
        super().__init__(name, Cube(), translate, rotate, scale)
        self.velocity = velocity
        self.groundHeight = -20
        self.viewPos = 15
        self.finished = False
    def update(self, deltaTime):
        position = self.transform["translate"]
        if position.y > self.groundHeight:
           self.velocity.y -= 10*9.87*deltaTime
        elif not self.velocity.y > 0:
            self.velocity.y = 0
            self.transform["translate"].y = self.groundHeight

        deltaX = self.velocity.x*deltaTime; deltaY = self.velocity.y*deltaTime; deltaZ = self.velocity.z*deltaTime
        self.transform["translate"].x += deltaX
        self.transform["translate"].y += deltaY
        if self.transform["translate"].y < self.groundHeight: self.transform["translate"].y = self.groundHeight
        self.transform["translate"].z += deltaZ

        if position.x < -2:
            self.transform["translate"].x = -2
        elif position.x > 2:
            self.transform["translate"].x = 2

        self.viewPos += -15*deltaTime
        if self.transform["translate"].z >= self.viewPos:
            if not self.finished:
                self.kill()
                self.viewPos = 15
            else:
                scene.remove_polyhedron(self.name)
                return

        self.add()
    def kill(self):
        global gameObjects
        for gameObject in gameObjects:
            gameObject.viewPos = 15
            gameObject.add()
        
        global view
        view = Matrix()
        view = view.translate(15,14,-15)
        view = view.rotate(Vector(0,1,0),45)

        self.transform["translate"] = Vector(0,0,0)
    def finish(self,test=None):
        self.finished = True
        self.shape.color = "green"
# endregion




# region Levels
gameObjects = []
level1 = [
    Player("player", velocity=Vector(0,0,-15), translate=Vector(0,0,0)),

    Obstacle("obstacle1", translate=Vector(-2,-20,-20)),
    Obstacle("obstacle2", translate=Vector(2,-19,-30), scale=Vector(1,2,1)),
    Obstacle("obstacle3", translate=Vector(0,-20,-40)),
    Obstacle("obstacle4", translate=Vector(2.2,-19,-50), scale=Vector(1,2,1)),
    Obstacle("obstacle5", translate=Vector(-2.2,-19,-50), scale=Vector(1,2,1)),

    Spike("obstacle6", translate=Vector(1,-20,-70)),
    Spike("obstacle7", translate=Vector(-1,-20,-70)),
    Spike("obstacle8", translate=Vector(-3,-20,-70)), 

    Finish("finish", translate=Vector(0,-18,-100), scale=(Vector(3,3,1)))
]
level2 = [
    Player("player", velocity=Vector(0,0,-15), translate=Vector(0,0,0)),

    Spike("obstacle1", translate=Vector(1,-20,-20)),
    Spike("obstacle2", translate=Vector(-1,-20,-20)),
    Spike("obstacle3", translate=Vector(-3,-20,-20)), 

    Obstacle("obstacle4", translate=Vector(0,-19,-30), scale=Vector(3,2,1)), 

    Obstacle("obstacle8", translate=Vector(0,-18,-45), scale=Vector(3,3,1)),
    Obstacle("obstacle9", translate=Vector(0,-18,-60), scale=Vector(3,3,1)),
    Obstacle("obstacle10", translate=Vector(0,-18,-80), scale=Vector(3,3,1)),
    Obstacle("obstacle11", translate=Vector(0,-18,-100), scale=Vector(3,3,1)),

    Finish("finish", translate=Vector(0,-18,-120), scale=(Vector(3,3,1)))
]
level3 = [
    Player("player", velocity=Vector(0,0,-15), translate=Vector(0,0,0)),

    Obstacle("obstacle1", translate=Vector(0,-20,-45), scale=Vector(3,1,3)),
    Obstacle("obstacle2", translate=Vector(0,-18,-60), scale=Vector(3,1,3)),
    Obstacle("obstacle3", translate=Vector(0,-16,-75), scale=Vector(3,1,3)),
    Obstacle("obstacle4", translate=Vector(0,-16,-90), scale=Vector(3,1,3)),
    Obstacle("obstacle5", translate=Vector(0,-16,-105), scale=Vector(3,1,3)),
    Obstacle("obstacle6", translate=Vector(0,-16,-120), scale=Vector(3,1,3)),

    Spike("obstacle7", translate=Vector(1,-20,-140)),
    Spike("obstacle8", translate=Vector(-1,-20,-140)),
    Spike("obstacle9", translate=Vector(-3,-20,-140)), 

    Finish("finish", translate=Vector(0,-10,-125), scale=(Vector(3,3,1)))
]
level4 = [
    Player("player", velocity=Vector(0,0,-15), translate=Vector(0,0,0)),

    Spike("obstacle1", translate=Vector(1,-20,-20)),
    Spike("obstacle2", translate=Vector(-1,-20,-20)),
    Spike("obstacle3", translate=Vector(-3,-20,-20)), 

    Obstacle("obstacle4", translate=Vector(0,-20,-45), scale=Vector(3,1,3)),
    Obstacle("obstacle5", translate=Vector(0,-18,-60), scale=Vector(3,1,3)),
    Obstacle("obstacle6", translate=Vector(0,-16,-75), scale=Vector(3,1,3)),
    Obstacle("obstacle7", translate=Vector(-2,-15,-83), scale=Vector(3,5,1)),
    Obstacle("obstacle8", translate=Vector(0,-16,-90), scale=Vector(3,1,3)),
    Obstacle("obstacle9", translate=Vector(-2,-15,-97), scale=Vector(3,5,1)),
    Obstacle("obstacle10", translate=Vector(0,-16,-105), scale=Vector(3,1,3)),
    Obstacle("obstacle11", translate=Vector(-2,-15,-112), scale=Vector(3,5,1)),
    Obstacle("obstacle12", translate=Vector(0,-16,-120), scale=Vector(3,1,3)),

    Spike("obstacle14", translate=Vector(1,-20,-75)),
    Spike("obstacle15", translate=Vector(-1,-20,-75)),
    Spike("obstacle16", translate=Vector(-3,-20,-75)), 

    Finish("finish", translate=Vector(0,-8,-125), scale=(Vector(3,3,1)))
]
level5 = [
    Player("player", velocity=Vector(0,0,-15), translate=Vector(0,0,0)),

    Spike("obstacle1", translate=Vector(1,-20,-20)),
    Spike("obstacle2", translate=Vector(-1,-20,-20)),
    Spike("obstacle3", translate=Vector(-3,-20,-20)),

    Obstacle("obstacle4", translate=Vector(-1,-16,-40), scale=Vector(2,5,1)),
    Obstacle("obstacle5", translate=Vector(2,-18,-40), scale=Vector(1,3,1)),

    Obstacle("obstacle6", translate=Vector(1,-16,-60), scale=Vector(2,5,1)),
    Obstacle("obstacle7", translate=Vector(-2,-18,-60), scale=Vector(1,3,1)),

    Obstacle("obstacle8", translate=Vector(0,-18,-80), scale=Vector(3,3,1)),

    Obstacle("obstacle9", translate=Vector(3,-16,-100), scale=Vector(1,5,1)),
    Obstacle("obstacle10", translate=Vector(-2,-16,-100), scale=Vector(1,5,1)),

    Obstacle("obstacle11", translate=Vector(0,-18,-110), scale=Vector(3,3,1)),

    Spike("obstacle12", translate=Vector(1,-20,-140)),
    Spike("obstacle13", translate=Vector(-1,-20,-140)),
    Spike("obstacle14", translate=Vector(-3,-20,-140)), 

    Finish("finish", translate=Vector(0,-8,-125), scale=(Vector(3,3,1)))
]
level6 = [
    Player("player", velocity=Vector(0,0,-15), translate=Vector(0,0,0)),

    Obstacle("obstacle1", translate=Vector(0,-16,-45), scale=Vector(3,1,10)),

    Spike("obstacle2", translate=Vector(1,-20,-60)),
    Spike("obstacle3", translate=Vector(-1,-20,-60)),
    Spike("obstacle4", translate=Vector(-3,-20,-60)),

    Obstacle("obstacle5", translate=Vector(0,-16,-75), scale=Vector(3,1,10)),
    Obstacle("obstacle6", translate=Vector(0,-12,-105), scale=Vector(3,1,10)),

    Spike("obstacle7", translate=Vector(1,-20,-130)),
    Spike("obstacle8", translate=Vector(-1,-20,-130)),
    Spike("obstacle9", translate=Vector(-3,-20,-130)),

    Finish("finish", translate=Vector(0,-4,-125), scale=(Vector(3,3,1)))
]
level7 = [
    Player("player", velocity=Vector(0,0,-15), translate=Vector(0,0,0)),

    Obstacle("obstacle1", translate=Vector(0,-18,-45)),
    Obstacle("obstacle2", translate=Vector(0,-16,-60)),
    Obstacle("obstacle3", translate=Vector(0,-14,-75)),
    Obstacle("obstacle4", translate=Vector(0,-12,-90)),
    Obstacle("obstacle5", translate=Vector(0,-10,-105)),
    Obstacle("obstacle6", translate=Vector(0,-8,-120)),

    Spike("obstacle7", translate=Vector(1,-20,-150)),
    Spike("obstacle8", translate=Vector(-1,-20,-150)),
    Spike("obstacle9", translate=Vector(-3,-20,-150)),

    Finish("finish", translate=Vector(0,-4,-125), scale=(Vector(3,3,1)))
]
level8 = [
    Player("player", velocity=Vector(0,0,-15), translate=Vector(0,0,0)),
    Finish("finish", translate=Vector(0,-20,-500), scale=(Vector(1,1,1)))
]
# endregion




"""INITIALIZE SCENE"""
scene = None
def init(level = 1):
    global scene
    scene = Scene()
        
    global gameObjects
    if level == 1: gameObjects = deepcopy(level1)
    elif level == 2: gameObjects = deepcopy(level2)
    elif level == 3: gameObjects = deepcopy(level3)
    elif level == 4: gameObjects = deepcopy(level4)
    elif level == 5: gameObjects = deepcopy(level5)
    elif level == 6: gameObjects = deepcopy(level6)
    elif level == 7: gameObjects = deepcopy(level7)
    elif level == 8: gameObjects = deepcopy(level8)
    else: gameObjects = deepcopy(level1)

    for gameObject in gameObjects:
        gameObject.add()
"""INITIALIZE SCENE"""




""" RENDER LOOP """
def render(
    playerColor, 
    floorColor,
    backgroundColor,
    level = 1, 
):
    beginGrfx(SCR_WIDTH, SCR_HEIGHT) # Viewport dimensions

    global scene
    init(level)
    if playerColor: gameObjects[0].shape.color = playerColor

    global view
    view = Matrix()
    view = view.translate(15,14,-15)
    view = view.rotate(Vector(0,1,0),45)
    currFrame = None; prevFrame = time(); deltaTime = None; ended = False

    while 0 == 0:
        currFrame = time()
        deltaTime = currFrame - prevFrame
        prevFrame = time()

        listen()
        processInput()

        for gameObject in gameObjects:
            gameObject.update(deltaTime)

        view = view.translate(15*deltaTime*0.7071, 0, 15*deltaTime*0.7071)
            
        # Update buffers
        if gameObjects[0].finished: 
            if not ended: 
                clear()
                setColor(backgroundColor); fillRectangle(0,0,SCR_WIDTH,SCR_HEIGHT)
                model = Matrix()
                model = model.scale(3,0,41)
                model = model.translate(-1.5,-20,gameObjects[0].viewPos+45)
                Cube(model,floorColor).draw() # Ground
                scene.draw()
            ended = True
            drawTitle("Level Complete!")
            drawTitle("Press E to exit.", 102)
            global e_key
            if e_key.down: return
        else:
            clear()
            setColor(backgroundColor); fillRectangle(0,0,SCR_WIDTH,SCR_HEIGHT)
            model = Matrix()
            model = model.scale(3,0,41)
            model = model.translate(-1.5,-20,gameObjects[0].viewPos+45)
            Cube(model,floorColor).draw() # Ground
            scene.draw()
        update()
    scene.remove_all()
""" RENDER LOOP """





