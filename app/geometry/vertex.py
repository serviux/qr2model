"""Helper classes containing information about vertices and the order in which they are generated in the Mesh Constructor"""
from dataclasses import dataclass
from enum import IntEnum

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

    def to_list(self) -> list:
        """Converts vertex to a list in order x,y,z"""
        return [self.x, self.y, self.z]
    
    def is_below(self, other_vertex: 'Vertex') -> bool:
        """
        Check if the current vertex is below another given vertex.

        :param other_vertex: The vertex to compare against.
        :return: True if this vertex's coordinates are all less than the other vertex's coordinates.
        """
        return self.x < other_vertex.x and self.y < other_vertex.y and self.z < other_vertex.z