"""Helper classes containing information about vertices and the order in which they are generated in the Mesh Constructor"""
from dataclasses import dataclass
from enum import IntEnum
from math import sqrt

class VERTEX_ORDER(IntEnum):
    """An enumeration of vertices generated """
    NORTH_WEST:int = 0
    SOUTH_WEST:int = 1
    NORTH_EAST:int = 2
    SOUTH_EAST:int = 3

@dataclass
class Vertex:
    """Class for keeping track of a vertex's coordinates"""
    x:int = 0
    y:int = 0
    z:int = 0
    idx:int = None
    def transform(self, a:int, b:int, c:int) ->  'Vertex':
        """Transforms the vertex's coordinates by a given matrix"""
        self.x += a
        self.y += b
        self.z += c
        return self

    def scale(self, a:int, b:int, c:int) -> 'Vertex':
        """Scales the vertex's coordinates by a given matrix"""
        self.x *= a
        self.y *= b
        self.z *= c
        return self

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    
    def __eq__(self, other: 'Vertex') -> bool:
        if isinstance(other, Vertex):
            return (self.x == other.x and self.y == other.y and self.z == other.z)
        raise(NotImplemented("Object comparison for Vertex and type is not implemented"))

    def to_list(self) -> list:
        """Converts vertex to a list in order x,y,z"""
        return [self.x, self.y, self.z]
    
    def check_geo_constraints(self, other_vertex: 'Vertex') -> bool:
        """
        Check if the current vertex is directly below another given vertex.

        :param other_vertex: The vertex to compare against.
        :return: True if this vertex's coordinates are all less than the other vertex's coordinates.
        """
        return self.x == other_vertex.x and self.y == other_vertex.y and self.z < other_vertex.z
    
    def dist_from_other(self, other_vertex: 'Vertex') -> float:
        """Calculates the distance between two vertices"""
        return sqrt((other_vertex.x-  self.x ) ** 2 + (other_vertex.y - self.y) ** 2 + (other_vertex.z - self.z) ** 2)