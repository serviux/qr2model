"""A helper class for containing the information about plane objects which are used during the mesh construction process"""

from dataclasses import dataclass
from typing import Iterable
from .vertex import Vertex
from .vertex import VERTEX_ORDER


@dataclass
class Plane:
    """A plane in 3D space."""
    north_west: Vertex
    south_west: Vertex
    north_east: Vertex
    south_east: Vertex
    
    @classmethod
    def from_iterable(cls, iterable: Iterable['Vertex']) -> 'Plane':
        """
        Create a new plane instance from an iterable of vertices.

        :param iterable: An iterable containing four vertices in the order NORTH_WEST, SOUTH_WEST, top_right, bottom_right.
        :return: A new Plane instance created from the given vertices.
        """
        return cls(
            north_west=iterable[VERTEX_ORDER.NORTH_WEST],
            south_west=iterable[VERTEX_ORDER.SOUTH_WEST],
            north_east=iterable[VERTEX_ORDER.NORTH_EAST],
            south_east=iterable[VERTEX_ORDER.SOUTH_EAST]
        )

    def is_below(self, other_plane: 'Plane') -> bool:
        """
        Check if the current plane's vertices are all less than another given plane's vertices.

        :param other_plane: The plane to compare against.
        :return: True if each vertex of this plane has coordinates less than the corresponding vertex of the other plane.
        """
        return (self.north_west.is_below(other_plane.north_west) and
                self.south_west.is_below(other_plane.SOUTH_WEST) and
                self.north_east.is_below(other_plane.top_right) and
                self.south_east.is_below(other_plane.bottom_right))

