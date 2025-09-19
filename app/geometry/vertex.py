from dataclasses import dataclass
from enum import Enum

class VERTEX_ORDER(Enum):
    """An enumeration of vertices generated """
    TOP_LEFT = 0
    BOTTOM_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_RIGHT = 3

@dataclass
class Vertex:
    """Class for keeping track of a vertex's coordinates"""
    x:float = 0
    y:float = 0 
    z:float = 0

    def transform(self, a:float, b:float, c:float) ->  None:
        """Transforms the vertex's coordinates by a given matrix"""
        self.x += a
        self.y += b
        self.z += c

    def scale(self, a:float, b:float, c:float) -> None:
        """Scales the vertex's coordinates by a given matrix"""
        self.x *= a
        self.y *= b
        self.z *= c

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def to_list(self) -> list:
        return [self.x, self.y, self.z]
    
    def is_below(self, other_vertex: 'Vertex') -> bool:
        """
        Check if the current vertex is below another given vertex.

        :param other_vertex: The vertex to compare against.
        :return: True if this vertex's coordinates are all less than the other vertex's coordinates.
        """
        return self.x < other_vertex.x and self.y < other_vertex.y and self.z < other_vertex.z