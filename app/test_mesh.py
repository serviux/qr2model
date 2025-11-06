import numpy as np
from stl import mesh

def main():

    # Define the 8 vertices of the cube
    vertices = np.array([\
        [-1, -1, -1],
        [+1, -1, -1],
        [+1, +1, -1],
        [-1, +1, -1],
        [-1, -1, +1],
        [+1, -1, +1],
        [+1, +1, +1],
        [-1, +1, +1]])
    # Define the 12 triangles composing the cube
    faces = np.array([\
        [0,3,1],
        [1,3,2],
        [0,4,7],
        [0,7,3],
        [4,5,6],
        [4,6,7],
        [5,1,2],
        [5,2,6],
        [2,3,6],
        [3,7,6],
        [0,1,5],
        [0,5,4]])
    test1 = []
    test2 = []
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            test1.append(vertices[f[j],:])
            test2.append(vertices[f[j]])
            cube.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "cube.stl"
    for i, _ in enumerate(test1):
        print(f"test1: {test1[i]}, test2: {test2[i]}, equal? {test1[i]==test2[i]}")

    cube.save('cube.stl')


if __name__ == "__main__":
    main()