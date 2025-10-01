
from stl import mesh
from geometry.vertex import VERTEX_ORDER
from geometry.vertex import Vertex
from geometry.plane import Plane
import numpy as np
import qrcode
import copy
from dataclasses import dataclass



@dataclass
class MeshConstructionParams: 
    """Handles the parameters needed to construct the mesh for the qr code"""
    size:float = 0
    depth:float = 0
    true_depth:float = 0

    def is_directly_above(self, other:Vertex) -> bool:
        """Checks if the other vertex is on the same x and y coordinate and is above the current z coordinate"""
        return (self.x == other.x and self.y == other.y and self.z < other.z)



class QRGenerator3d: 


    def __init__(self, params:MeshConstructionParams, qr_message:str):
        self.params = params
        self.qr_message = qr_message
        self.vertices = np.empty((0))
        self.faces = np.empty((0))


    def generate_qr_code(self, message:str) -> qrcode.QRCode:
        """Generate a QR code from the given message"""
        qr = qrcode.QRCode(
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4)

        qr.add_data(message)
        qr.make() 

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("temp.png")

        print("Saved to temp.png")
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


                
                layer_one = [vert.scale(params.size, params.size, 1) for vert in layer_one]

                # transform the vertices on the x and y plane based upon the above loop iterations
                layer_one = [vert.transform(j,starting_idx,0) for vert in layer_one]

                #make a copy of layer 1 to scale in the z axis, so the final mesh has some depth 
                layer_two  = copy.deepcopy(layer_one)
                layer_two = [vert.transform(0,0, params.depth) for vert in layer_two]
                
                np.append(self.vertices, layer_one)
                np.append(self.vertices, layer_two)

                if toggle: 
                    layer_three = copy.deepcopy(layer_two)
                    layer_three = [vert.transform(0,0, params.true_depth) for vert in layer_three]
                    np.append(self.vertices, layer_three)
        

    def _build_faces(self) -> None: 
        """Generate the faces of the 3d model from the list of vertices"""


        middle_idx_displacement:int = 4
        top_idx_displacement:int = 8

        number_of_ahead_groups_processed = 0 
        
        for starting_idx in range(0, len(self.vertices), 4):
            
            if number_of_ahead_groups_processed > 0 : 
                number_of_ahead_groups_processed -= 1
                continue
            
    
            

            #Determine if third grouping is above the first_group in order to determine the number of verticle walls to make.
            first_group:Plane =   Plane.from_iterable(self.vertices[starting_idx:starting_idx+4])
            third_group:Plane =   Plane.from_iterable(self.vertices[starting_idx+top_idx_displacement:starting_idx+12])

            bottom_faces = self._build_horizontal_faces(starting_idx)
            middle_faces = self._build_verticle_faces(starting_idx, 4) 

            np.append(self.faces, bottom_faces)
            np.append(self.faces, middle_faces)



            
            if first_group.is_below(third_group):
                third_group = self._build_verticle_faces(starting_idx + 4, 8)
                top_group = self._build_horizontal_faces(starting_idx + 8)
                np.append(self.faces, third_group) 
                np.append(self.faces, top_group) 
                number_of_ahead_groups_processed = 2
            else:
                top_group = self._build_horizontal_faces(starting_idx + 4)
                np.append(self.faces, top_group)
                number_of_ahead_groups_processed = 1





 

    def _build_horizontal_faces(self, starting_idx: int, idx_displacement: int = 0) -> np.array:
        """Builds the horizontal faces for a given module in the QR code. """
        
        
        displacement_factor:int = starting_idx + idx_displacement

        return np.array([ [VERTEX_ORDER.BOTTOM_LEFT + displacement_factor,
                                       VERTEX_ORDER.TOP_LEFT + displacement_factor ,
                                       VERTEX_ORDER.BOTTOM_RIGHT + displacement_factor], 

                                      [VERTEX_ORDER.BOTTOM_RIGHT + displacement_factor,
                                       VERTEX_ORDER.TOP_RIGHT + displacement_factor,
                                       VERTEX_ORDER.TOP_LEFT + displacement_factor]], ndmin=(2,3))
    
    
    def _build_verticle_faces(self, starting_idx:int, idx_displacement:int = 0) -> np.array:
        """Constructs a set of verticle faces for a given qr code"""
        displacement_factor:int = starting_idx + idx_displacement

        return np.array([ 
                
                # west side faces
                                      [ VERTEX_ORDER.TOP_LEFT + displacement_factor,
                                        VERTEX_ORDER.BOTTOM_LEFT  + displacement_factor,
                                        VERTEX_ORDER.TOP_LEFT + starting_idx],  

                                      [ VERTEX_ORDER.TOP_LEFT + starting_idx ,
                                        VERTEX_ORDER.BOTTOM_LEFT + starting_idx ,
                                        VERTEX_ORDER.BOTTOM_LEFT  + displacement_factor] ,                                      
                                        
                # south side faces
                                     [ VERTEX_ORDER.BOTTOM_LEFT + displacement_factor,
                                        VERTEX_ORDER.BOTTOM_RIGHT  + displacement_factor,
                                        VERTEX_ORDER.BOTTOM_RIGHT + starting_idx],  

                                     [ VERTEX_ORDER.BOTTOM_RIGHT + starting_idx ,
                                        VERTEX_ORDER.BOTTOM_LEFT + starting_idx ,
                                        VERTEX_ORDER.BOTTOM_LEFT  + displacement_factor] ,   
                # east side faces

                                    [ VERTEX_ORDER.TOP_RIGHT + displacement_factor,
                                        VERTEX_ORDER.BOTTOM_RIGHT  +displacement_factor,
                                        VERTEX_ORDER.BOTTOM_RIGHT + starting_idx],  

                                      [ VERTEX_ORDER.BOTTOM_RIGHT + starting_idx ,
                                        VERTEX_ORDER.TOP_RIGHT + starting_idx ,
                                        VERTEX_ORDER.TOP_RIGHT  + displacement_factor] ,

                #north side faces 

                                    [ VERTEX_ORDER.TOP_RIGHT + displacement_factor,
                                        VERTEX_ORDER.TOP_LEFT  + displacement_factor,
                                        VERTEX_ORDER.TOP_LEFT + starting_idx],  

                                      [ VERTEX_ORDER.TOP_LEFT + starting_idx ,
                                        VERTEX_ORDER.TOP_RIGHT + starting_idx ,
                                        VERTEX_ORDER.TOP_RIGHT  + displacement_factor] ,
                                        
                                        ], ndmin=(2,3))


    
        

        

    def construct_mesh(self, params:MeshConstructionParams, qr:qrcode.QRCode) -> mesh.Mesh: 
        

        data = np.zeros(100, dtype=mesh.Mesh.dtype)
        qr_mesh = mesh.Mesh(data, remove_empty_areas=False)





    
