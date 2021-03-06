"""
ground.py

Sets up the ground for the scene with a grass texture.
"""

import numpy as np
from OpenGL.GL import *
from object import SceneObject

GRASS_TEXTURE_PATH = b"grass_texture.jpg"

class Ground(SceneObject):
    """
    Class representing the ground in the scene.
    """

    def __init__(self, shader_program):
        """
        Contructor. Tesselates the shape, sets normals, texture UV-coordinates
        and elements. Sets up material properties. Loads the grass texture.
        Buffers all the data to the GPU.

        :param shader_program: A unique ID for the shader_program to be used
                               with this object
        """
        self.tessellate(10, 3)

        self.normals = np.array([0.0, 1.0, 0.0] * (len(self.vertices)//3),
                                dtype=np.float32)

        self.k_ambient = np.array([0.4, 0.6, 0.2], dtype=np.float32)
        self.k_diffuse = np.array([0.2, 0.3, 0.1], dtype=np.float32)
        self.k_specular = np.array([0.1, 0.15, 0.05], dtype=np.float32)
        self.shininess = 0.0

        self.load_texture(GRASS_TEXTURE_PATH)
        self.set_buffers(shader_program)

    def tessellate(self, divisions, tex_repetitions):
        """
        Calculates the vertices, triangles and the texture UV-coordinates at
        the vertices of the ground object. The ground is represented as a quad.

        :param divisions: The number of subdivisions for tessellation
        :param tex_repititions: The number of times the texture is to be
                                repeated over the object
        """
        vertices = []
        elements = []
        texture_uv = []
        step = 2 / divisions

        # Calculate vertices and UV values
        for i in np.arange(-1.0, 1.0 + step, step):
            for j in np.arange(-1.0, 1.0 + step, step):
                vertices.append([i, 0.0, j])
                texture_uv.append([(tex_repetitions / 2) * (i + 1),
                                   (tex_repetitions / 2) * (j + 1)])

        vertices = [x for vertex in vertices for x in vertex]
        texture_uv = [x for tex_coord in texture_uv for x in tex_coord]

        # Calculate the triangles making up the object
        for i in range(divisions):
            for j in range(divisions):
                elements.append(i * (divisions + 1) + j)
                elements.append(i * (divisions + 1) + (j + 1))
                elements.append((i + 1) * (divisions + 1) + (j + 1))
                elements.append((i + 1) * (divisions + 1) + (j + 1))
                elements.append((i + 1) * (divisions + 1) + j)
                elements.append(i * (divisions + 1) + j)

        self.vertices = np.array(vertices, dtype=np.float32)
        self.elements = np.array(elements, dtype=np.uint16)
        self.texture_uv = np.array(texture_uv, dtype=np.float32)
