
from stl import mesh
from vertex import Vertex
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
        for i,  module in enumerate(qr.modules):
            for j, toggle in enumerate(module):


                #determine vertices of the bottom part of the cell in the qr code
                #layer_one will always be a face. 
                layer_one = [
                            Vertex(0,0,0), # bot left
                            Vertex(0,1,0), # top left
                            Vertex(1,0,0), # bot right
                            Vertex(1,1,0)  # top right
                   
                            ]


                
                layer_one = [vert.scale(params.size, params.size, 1) for vert in layer_one]

                # transform the vertices on the x and y plane based upon the above loop iterations
                layer_one = [vert.transform(j,i,0) for vert in layer_one]

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




        is_bottom_group = True
        is_top_group = False

        number_of_ahead_groups_processed = 0 
        
        for i in range(0, len(self.vertices), 4):
            
            if(number_of_ahead_groups_processed > 0): 
                number_of_ahead_groups_processed -= 1
                continue
    
            
            first_group = self.vertices[i:i+4]
            second_group = self.vertices[i+4:i+8]
            third_group = self.vertices[i+8:i+12]


            #construct faces for bottom layer



            bottom_faces = np.array([ [0 + i,
                                       2 + i ,
                                       1 + i], 
                                      [1 + i,
                                       3 + i,
                                       2 + i]], ndmin=(2,3))
            


            

        

    def construct_mesh(self, params:MeshConstructionParams, qr:qrcode.QRCode) -> mesh.Mesh: 
        

        data = np.zeros(100, dtype=mesh.Mesh.dtype)
        qr_mesh = mesh.Mesh(data, remove_empty_areas=False)





    
