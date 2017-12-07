"""
ground.py

Sets up the ground for the scene with a grass texture.
"""

import numpy as np
import glfw
from OpenGL.GL import *
from object import SceneObject

GROUND_SIZE = 30.0
GRASS_TEXTURE_PATH = b"GrassGreenTexture0006.jpg"

class Ground(SceneObject):
    """
    Class representing the ground in the scene.
    """
    
    def __init__(self):
        self.vertices = np.array([-GROUND_SIZE, 0.0, GROUND_SIZE,
                                  GROUND_SIZE, 0.0, GROUND_SIZE,
                                  GROUND_SIZE, 0.0, -GROUND_SIZE,
                                  -GROUND_SIZE, 0.0, -GROUND_SIZE],
                                 dtype=np.float32)

        self.elements = np.array([0, 1, 2,
                                  2, 3, 0], dtype=np.uint16)

        self.texture_uv = np.array([0.0, 0.0,
                                    2.0, 0.0,
                                    2.0, 2.0,
                                    0.0, 2.0], dtype=np.float32)

        self.normals = np.array([0.0, 1.0, 0.0] * (len(self.vertices)//3),
                                dtype=np.float32)

        self.k_ambient = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        self.k_diffuse = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        self.k_specular = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        self.shininess = 8.0

        self.load_texture(GRASS_TEXTURE_PATH)
        self.set_buffers()
