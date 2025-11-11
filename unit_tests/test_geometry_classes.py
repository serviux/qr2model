from app.geometry import Vertex
from app.geometry import VERTEX_ORDER
from app.geometry import Plane


def test_vertex_is_constrained(): 
    a:Vertex = Vertex(0,0,1)
    b:Vertex = Vertex(0,0,2)
    assert(a.check_geo_constraints(b))

def test_vertex_is_not_constrained(): 
    a:Vertex = Vertex(1,2,4)
    b:Vertex = Vertex(0,0,2)
    assert(not a.check_geo_constraints(b))

def test_vertex_distance():
    a:Vertex = Vertex(0,0,1)
    b:Vertex = Vertex(0,0,2)
    assert(a.dist_from_other(b) == 1)

def test_vertex_distance2():
    a:Vertex = Vertex(-1,0,1)
    b:Vertex = Vertex(2,0,2)
    assert(a.dist_from_other(b) > 1)

def test_vertex_transform():
    a:Vertex = Vertex(0,0,1)
    a.transform(1,1,1)
    assert(a.x ==1 and a.y==1 and a.z == 2)

def test_vertex_scale(): 
    a:Vertex = Vertex(1,1,1)
    a.scale(2,3,5)
    assert(a.x == 2, a.y ==3, a.z == 5)

def test_vertex_to_list():
    a:Vertex = Vertex(1,2,3)
    a_list = a.to_list()
    assert(type(a_list) == list)
    assert(a.x == a_list[0] and a.y == a_list[1] and a.z == a_list[2])

def test_plane_from_iterable():
    vertices  = (Vertex(0,0,0), Vertex(1,0,0), Vertex(1,1,0), Vertex(0,1,0))
    plane = Plane.from_iterable(vertices)
    assert(plane.north_west == vertices[VERTEX_ORDER.NORTH_WEST] and 
           plane.south_west == vertices[VERTEX_ORDER.SOUTH_WEST] and 
           plane.south_east == vertices[VERTEX_ORDER.SOUTH_EAST] and
           plane.north_east == vertices[VERTEX_ORDER.NORTH_EAST])
    
def test_plane_is_geo_constrained():
    plane  = Plane.from_iterable ([Vertex(0,0,0), Vertex(1,0,0), Vertex(1,1,0), Vertex(0,1,0)])
    plane2  = Plane.from_iterable ([Vertex(0,0,1), Vertex(1,0,1), Vertex(1,1,1), Vertex(0,1,1)])
    assert(plane.check_geo_constraints(plane2))

def test_plane_is_not_geo_constrained():
    plane  = Plane.from_iterable ([Vertex(0,0,0), Vertex(1,0,0), Vertex(1,1,0), Vertex(0,1,0)])
    plane2  = Plane.from_iterable ([Vertex(20,0,1), Vertex(1,15,1), Vertex(1,1,1), Vertex(0,1,1)])
    assert(not plane.check_geo_constraints(plane2))

def test_plane_distance_calc():
    plane  = Plane.from_iterable ([Vertex(0,0,0), Vertex(1,0,0), Vertex(1,1,0), Vertex(0,1,0)])
    plane2  = Plane.from_iterable ([Vertex(20,0,1), Vertex(1,15,1), Vertex(1,1,1), Vertex(0,1,1)])
    assert(plane.distance_to_other(plane2) > 1)