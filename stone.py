"""
ground.py

Sets up the stones that make up Stonehenge.
"""

import numpy as np
from OpenGL.GL import *
from object import SceneObject

STONE_TEXTURE_PATH = b"stone_texture.jpg"

class Stone(SceneObject):
    """
    Class representing a stone in the scene.
    """

    def __init__(self, shader_program):
        self.tessellate(10)

        self.k_ambient = np.array([0.3, 0.3, 0.3], dtype=np.float32)
        self.k_diffuse = np.array([0.2, 0.2, 0.2], dtype=np.float32)
        self.k_specular = np.array([0.1, 0.1, 0.1], dtype=np.float32)
        self.shininess = 0.0

        self.load_texture(STONE_TEXTURE_PATH)
        self.set_buffers(shader_program)

    def tessellate(self, divisions):
        start, end = -1.0, 1.0
        step = (end - start) / divisions

        vertices = []
        normals = []
        texture_uv = []
        elements = []

        # X = -1
        num_vertices = len(vertices)
        for i in np.arange(start, end+step, step):
            for j in np.arange(start, end+step, step):
                vertices.append([-1.0, i, j])
                texture_uv.append([1 / (end - start) * (i - start),
                                   1 / (end - start) * (j - start)])
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
                texture_uv.append([1 / (end - start) * (i - start),
                                   1 / (end - start) * (j - start)])
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
                texture_uv.append([1 / (end - start) * (i - start),
                                   1 / (end - start) * (j - start)])
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
                texture_uv.append([1 / (end - start) * (i - start),
                                   1 / (end - start) * (j - start)])
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
                texture_uv.append([1 / (end - start) * (i - start),
                                   1 / (end - start) * (j - start)])
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
                texture_uv.append([1 / (end - start) * (i - start),
                                   1 / (end - start) * (j - start)])
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
        texture_uv = [x for tex_coord in texture_uv for x in tex_coord]
        normals = [x for normal in normals for x in normal]

        self.vertices = np.array(vertices, dtype=np.float32)
        self.elements = np.array(elements, dtype=np.uint16)
        self.texture_uv = np.array(texture_uv, dtype=np.float32)
        self.normals = np.array(normals, dtype=np.float32)
