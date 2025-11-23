"""Generates a qrcode using the qr library and uses the modules of the qr code to construct a mesh which is saved to an stl file"""


import copy
from dataclasses import dataclass
import numpy as np
import qrcode
from stl import mesh
from geometry.vertex import VERTEX_ORDER
from geometry.vertex import Vertex
from geometry.plane import Plane





@dataclass
class MeshConstructionParams:
    """Handles the parameters needed to construct the mesh for the qr code"""
    size:float = 0
    depth:float = 0
    true_depth:float = 0

class QRGenerator3d:
    """Generates the qrcode and Mesh objects"""
    def __init__(self, params:MeshConstructionParams, qr_message:str):
        self.params = params
        self.qr_message = qr_message
        self.vertices = np.empty((0))
        self.faces = np.empty((0), dtype=np.dtype(np.int64))


    def generate_qr_code(self, message:str) -> qrcode.QRCode:
        """Generate a QR code from the given message"""
        qr = qrcode.QRCode(
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4)

        qr.add_data(message)
        qr.make()


        return qr
    

    def _generate_vertices(self, params:MeshConstructionParams, qr:qrcode.QRCode) -> None:
        """Generate vertices from the given QR code"""
        #loop through each row of the QR code and check if the module is a black or white pixel
        #and generate a series of vertices for 

        for starting_idx,  module in enumerate(qr.modules):
            for j, toggle in enumerate(module):


                #determine vertices of the bottom part of the cell in the qr code
                #layer_one will always be a face.
                layer_one = [
                            
                            Vertex(0,1,0), # top left
                            Vertex(0,0,0), # bot left
                            Vertex(1,1,0),  # top right
                            Vertex(1,0,0) # bot right
                   
                            ]

               

                for i, vert in  enumerate(layer_one):
                   layer_one[i] = vert.scale(params.size, params.size, 1)
                   layer_one[i] = vert.transform(j,starting_idx,0)


                layer_two  = copy.deepcopy(layer_one)
                
                for i, vert in enumerate(layer_two):
                   layer_two[i] = vert.transform(0,0, params.depth)

                    
                   
                self.vertices = np.append(self.vertices, layer_one, axis=0)
                self.vertices = np.append(self.vertices, layer_two, axis=0)

                if toggle:
                    layer_three = copy.deepcopy(layer_two)
                    for i, vert in enumerate(layer_three):
                        layer_three[i] = vert.transform(0,0, params.true_depth)

                    self.vertices = np.append(self.vertices, layer_three)


    def _index_vertices(self) -> None:
        """fills the idx property of each vertex object"""
        for i, _ in enumerate(self.vertices):
            self.vertices[i].idx = i


    def _build_faces(self) -> None:
        """Generate the faces of the 3d model from the list of vertices"""
        number_of_ahead_groups_processed = 0

        for starting_idx in range(0, len(self.vertices), 4):

            if number_of_ahead_groups_processed > 0 :
                number_of_ahead_groups_processed -= 1
                continue

            #Determine if third grouping is above the first_group in order to determine the number of vertical walls to make.
            first_group:Plane =   Plane.from_iterable(self.vertices[starting_idx:starting_idx+4])
            second_group:Plane =   Plane.from_iterable(self.vertices[starting_idx+4:starting_idx+8])
            third_group:Plane = None

            if starting_idx + 12 <= len(self.vertices):
                third_group:Plane =   Plane.from_iterable(self.vertices[starting_idx+8:starting_idx+12])
            
                
            bottom_faces = self._build_horizontal_faces(first_group)
            middle_faces = self._build_vertical_faces(first_group, second_group)


            self.faces = np.append(self.faces, bottom_faces)
            self.faces = np.append(self.faces, middle_faces)

            if third_group and first_group.check_geo_constraints(third_group):
                upper_faces = self._build_vertical_faces(second_group, third_group)
                top_faces = self._build_horizontal_faces(third_group)
                self.faces = np.append(self.faces, upper_faces)
                self.faces = np.append(self.faces, top_faces)
                number_of_ahead_groups_processed = 2
            else:
                top_group = self._build_horizontal_faces(second_group)
                self.faces = np.append(self.faces, top_group)
                number_of_ahead_groups_processed = 1



    def _build_horizontal_faces(self,  plane:Plane) -> np.array:
        """Builds the horizontal faces for a given module in the QR code. """
        
        
        part_one = [plane.south_west.idx, 
                    plane.north_west.idx,
                    plane.south_east.idx]
        part_two = [plane.south_east.idx,
                    plane.north_east.idx,
                    plane.north_west.idx]
        
        return np.array([ part_one, part_two])


    def _build_vertical_faces(self, lower_plane:Plane, upper_plane:Plane) -> np.array:
        """Constructs a set of vertical faces for a given qr code"""

        return np.array([

            #west side faces
                            [upper_plane.north_west.idx,
                             upper_plane.south_west.idx,
                             lower_plane.north_west.idx ],

                            [lower_plane.north_west.idx,
                             lower_plane.south_west.idx,
                             upper_plane.south_west.idx],

            #south side faces
                            [ upper_plane.south_west.idx,
                              upper_plane.south_east.idx,
                              lower_plane.south_east.idx],

                            [lower_plane.south_east.idx,
                             lower_plane.south_west.idx,
                             upper_plane.south_west.idx],

            #east side faces 
                            [upper_plane.north_east.idx,
                             upper_plane.south_east.idx,
                             lower_plane.south_east.idx],

                            [lower_plane.south_east.idx,
                             lower_plane.north_east.idx,
                             upper_plane.north_east.idx],

            #north side faces 
                            [upper_plane.north_east.idx, 
                             upper_plane.north_west.idx,
                             lower_plane.north_west.idx],

                            [lower_plane.north_west.idx,
                             lower_plane.north_east.idx,
                             upper_plane.north_east.idx]
                                       
                        ])
    

    def _reshape_face_list(self) -> None:
        """reshapes the faces list into the proper shape
        reshapes into  a 2d array of shape (n, 3) where n is the starting shape divided by 3"""
        face_list_len:int = self.faces.size
        self.faces = self.faces.reshape((face_list_len//3, 3))


    def construct_mesh(self, params:MeshConstructionParams, qr:qrcode.QRCode) -> mesh.Mesh:
        
        self._generate_vertices(params, qr)
        self._index_vertices()
        self._build_faces()
        self._reshape_face_list()


        vertices_as_list = [vert.to_list() for vert in self.vertices]
       
        qr_mesh = mesh.Mesh(np.zeros(self.faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(self.faces):
            for j in range(3):
                qr_mesh.vectors[i][j] = vertices_as_list[f[j]]
        
        return qr_mesh
    

    def save_mesh(self, qr_mesh:mesh.Mesh) -> None:
        """Saves the mesh to the given file name"""
        
        filename = f"qr_mesh_{hash(self)}.stl"
        qr_mesh.save(filename)
