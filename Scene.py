from Graphics import *
from copy import deepcopy

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

        self.polygons = []
        for polyhedron in self.polyhedrons:
            for polygon in polyhedron.polygons:
                self.polygons.append(polygon)

    def add_polyhedron(self, name: str, polyhedron: object):
        self.polyhedrons[name] = polyhedron
        self.polyhedronsList = list(self.polyhedrons.values())
    def remove_polyhedron(self, name: str):
        if self.polyhedrons.get(name) is None:
            return
        del self.polyhedrons[name]
        self.polyhedronsList = list(self.polyhedrons.values())

    def draw(self):
        self.depth_sort()
        for polyhedron in self.polyhedronsList:
            for polygon in polyhedron.polygons:
                if type(polyhedron.color) == str:
                    setColor(polyhedron.color)
                elif type(polyhedron.color) == list:
                    setColor(polyhedron.color[0], polyhedron.color[1], polyhedron.color[2]) 
                polygon.draw(polyhedron.model)
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