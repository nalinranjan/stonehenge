"""
boulder.py

Sets up the boulders among Stonehenge.
"""

import numpy as np
import math
from OpenGL.GL import *
from object import SceneObject

class Boulder(SceneObject):
    """
    Class representing a boulder in the scene.
    """

    def __init__(self, shader_program):
        self.tessellate(20)

        self.k_ambient = np.array([0.3, 0.3, 0.21], dtype=np.float32)
        self.k_diffuse = np.array([0.4, 0.5, 0.35], dtype=np.float32)
        self.k_specular = np.array([0.3, 0.3, 0.3], dtype=np.float32)
        self.shininess = 7.0

        self.set_buffers(shader_program)

    def tessellate(self, divisions):
        theta_step = 360 / divisions
        phi_step = 180 / divisions
        radius = 1.0

        vertices = []
        elements = []

        for theta in np.arange(0, 360, theta_step):
            for phi in np.arange(0, 180 + phi_step, phi_step):
                v = [math.sin(math.radians(theta)) * math.sin(math.radians(phi)),
                     math.cos(math.radians(phi)),
                     math.cos(math.radians(theta)) * math.sin(math.radians(phi))]
                vertices.append([radius * c for c in v])

        num_vertices = len(vertices)

        for i in range(divisions):
            for j in range(divisions):
                elements.append((i * (divisions + 1) + j) % num_vertices)
                elements.append((i * (divisions + 1) + (j + 1)) % num_vertices)
                elements.append(((i + 1) * (divisions + 1) + (j + 1)) % num_vertices)
                elements.append(((i + 1) * (divisions + 1) + (j + 1)) % num_vertices)
                elements.append(((i + 1) * (divisions + 1) + j) % num_vertices)
                elements.append((i * (divisions + 1) + j) % num_vertices)

        vertices = [x for vertex in vertices for x in vertex]

        self.vertices = np.array(vertices, dtype=np.float32)
        self.normals = np.array(vertices, dtype=np.float32)
        self.elements = np.array(elements, dtype=np.uint16)
