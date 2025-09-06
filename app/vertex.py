from dataclasses import dataclass


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