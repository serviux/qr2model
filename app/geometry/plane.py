"""A helper class for containing the information about plane objects which are used during the mesh construction process"""

from dataclasses import dataclass
from typing import Iterable
from .vertex import Vertex
from .vertex import VERTEX_ORDER


@dataclass
class Plane:
    """A plane in 3D space."""
    top_left: Vertex
    bottom_left: Vertex
    top_right: Vertex
    bottom_right: Vertex
    
    @classmethod
    def from_iterable(cls, iterable: Iterable['Vertex']) -> 'Plane':
        """
        Create a new plane instance from an iterable of vertices.

        :param iterable: An iterable containing four vertices in the order top_left, bottom_left, top_right, bottom_right.
        :return: A new Plane instance created from the given vertices.
        """
        return cls(
            top_left=iterable[VERTEX_ORDER.TOP_LEFT],
            bottom_left=iterable[VERTEX_ORDER.BOTTOM_LEFT],
            top_right=iterable[VERTEX_ORDER.TOP_RIGHT],
            bottom_right=iterable[VERTEX_ORDER.BOTTOM_RIGHT]
        )

    def is_below(self, other_plane: 'Plane') -> bool:
        """
        Check if the current plane's vertices are all less than another given plane's vertices.

        :param other_plane: The plane to compare against.
        :return: True if each vertex of this plane has coordinates less than the corresponding vertex of the other plane.
        """
        return (self.top_left.is_below(other_plane.top_left) and
                self.bottom_left.is_below(other_plane.bottom_left) and
                self.top_right.is_below(other_plane.top_right) and
                self.bottom_right.is_below(other_plane.bottom_right))

