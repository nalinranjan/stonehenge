"""
stone.py

Sets up the stones that make up Stonehenge.
"""

import numpy as np
from OpenGL.GL import *
from object import SceneObject

class Stone(SceneObject):
    """
    Class representing a stone in the scene.
    """

    def __init__(self, shader_program):
        """
        Contructor. Tesselates the shape, sets normals and elements. Sets up
        material properties. Buffers all the data to the GPU.

        :param shader_program: A unique ID for the shader_program to be used
                               with this object
        """
        self.tessellate(10)

        self.k_ambient = np.array([0.15, 0.25, 0.25], dtype=np.float32)
        self.k_diffuse = np.array([0.25, 0.3, 0.3], dtype=np.float32)
        self.k_specular = np.array([0.3, 0.3, 0.3], dtype=np.float32)
        self.shininess = 2.0

        self.set_buffers(shader_program)

    def tessellate(self, divisions):
        """
        Calculates the vertices, triangles and normals at the vertices of a
        stone object. A stone is represented as a cuboid.

        :param divisions: The number of subdivisions for tessellation
        """
        start, end = -1.0, 1.0
        step = (end - start) / divisions

        vertices = []
        normals = []
        elements = []

        # X = -1
        num_vertices = len(vertices)
        for i in np.arange(start, end+step, step):
            for j in np.arange(start, end+step, step):
                vertices.append([-1.0, i, j])
                normals.append([-1.0, 0.0, 0.0])
        
        for i in range(divisions):
            for j in range(divisions):
                elements.append(num_vertices + i * (divisions + 1) + j) # 0
                elements.append(num_vertices + i * (divisions + 1) + (j + 1)) # 1
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1)) # 4
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1)) # 4
                elements.append(num_vertices + (i + 1) * (divisions + 1) + j) # 3
                elements.append(num_vertices + i * (divisions + 1) + j) # 0

        # X = 1
        num_vertices = len(vertices)
        for i in np.arange(start, end+step, step):
            for j in np.arange(start, end+step, step):
                vertices.append([1.0, i, j])
                normals.append([1.0, 0.0, 0.0])

        for i in range(divisions):
            for j in range(divisions):
                elements.append(num_vertices + i * (divisions + 1) + j) # 0
                elements.append(num_vertices + (i + 1) * (divisions + 1) + j) # 3
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1)) # 4
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1)) # 4
                elements.append(num_vertices + i * (divisions + 1) + (j + 1)) # 1
                elements.append(num_vertices + i * (divisions + 1) + j) # 0

        # Y = -1
        num_vertices = len(vertices)
        for i in np.arange(start, end+step, step):
            for j in np.arange(start, end+step, step):
                vertices.append([i, -1.0, j])
                normals.append([0.0, -1.0, 0.0])
        
        for i in range(divisions):
            for j in range(divisions):
                elements.append(num_vertices + i * (divisions + 1) + j)
                elements.append(num_vertices + (i + 1) * (divisions + 1) + j)
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1))
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1))
                elements.append(num_vertices + i * (divisions + 1) + (j + 1))
                elements.append(num_vertices + i * (divisions + 1) + j)

        # Y = 1
        num_vertices = len(vertices)
        for i in np.arange(start, end+step, step):
            for j in np.arange(start, end+step, step):
                vertices.append([i, 1.0, j])
                normals.append([0.0, 1.0, 0.0])
        
        for i in range(divisions):
            for j in range(divisions):
                elements.append(num_vertices + i * (divisions + 1) + j)
                elements.append(num_vertices + i * (divisions + 1) + (j + 1))
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1))
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1))
                elements.append(num_vertices + (i + 1) * (divisions + 1) + j)
                elements.append(num_vertices + i * (divisions + 1) + j)

        # Z = -1
        num_vertices = len(vertices)
        for i in np.arange(start, end+step, step):
            for j in np.arange(start, end+step, step):
                vertices.append([i, j, -1.0])
                normals.append([0.0, 0.0, -1.0])
        
        for i in range(divisions):
            for j in range(divisions):
                elements.append(num_vertices + i * (divisions + 1) + j)
                elements.append(num_vertices + i * (divisions + 1) + (j + 1))
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1))
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1))
                elements.append(num_vertices + (i + 1) * (divisions + 1) + j)
                elements.append(num_vertices + i * (divisions + 1) + j)

        # Z = 1
        num_vertices = len(vertices)
        for i in np.arange(start, end+step, step):
            for j in np.arange(start, end+step, step):
                vertices.append([i, j, 1.0])
                normals.append([0.0, 0.0, 1.0])
        
        for i in range(divisions):
            for j in range(divisions):
                elements.append(num_vertices + i * (divisions + 1) + j)
                elements.append(num_vertices + (i + 1) * (divisions + 1) + j)
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1))
                elements.append(num_vertices + (i + 1) * (divisions + 1) + (j + 1))
                elements.append(num_vertices + i * (divisions + 1) + (j + 1))
                elements.append(num_vertices + i * (divisions + 1) + j)

        vertices = [x for vertex in vertices for x in vertex]
        normals = [x for normal in normals for x in normal]

        self.vertices = np.array(vertices, dtype=np.float32)
        self.elements = np.array(elements, dtype=np.uint16)
        self.normals = np.array(normals, dtype=np.float32)
