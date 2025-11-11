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

    def check_geo_constraints(self, other_plane: 'Plane') -> bool:
        """
        Check if the current plane's vertices are all properly constrained underneath the other plane.

        :param other_plane: The plane to compare against.
        :return: True if each vertex of this plane has coordinates less than the corresponding vertex of the other plane.
        """
        return (self.north_west.check_geo_constraints(other_plane.north_west) and
                self.south_west.check_geo_constraints(other_plane.south_west) and
                self.north_east.check_geo_constraints(other_plane.north_east) and
                self.south_east.check_geo_constraints(other_plane.south_east))
    

    def distance_to_other(self, other_plane: 'Plane') -> float:
        """ gets the distance of all vertices to the other plane's vertices"""
        return (self.north_east.dist_from_other(other_plane.north_east) +
            self.north_west.dist_from_other(other_plane.north_west) +
            self.south_east.dist_from_other(other_plane.south_east) +
            self.south_west.dist_from_other(other_plane.south_west)
        ) / 4

        

