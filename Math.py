from math import *




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