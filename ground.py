"""
ground.py

Sets up the ground for the scene with a grass texture.
"""

import numpy as np
import glfw
from OpenGL.GL import *
from object import SceneObject

GROUND_SIZE = 100.0
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
                                    1.0, 0.0,
                                    1.0, 1.0,
                                    0.0, 1.0], dtype=np.float32)

        self.normals = np.array([0.0, 1.0, 0.0] * (len(self.vertices)//3),
                                dtype=np.float32)

        self.load_texture(GRASS_TEXTURE_PATH)
        self.vao = self.set_buffers()

if __name__ == "__main__":
    if not glfw.init():
        exit()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    width, height = 1280, 720

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(width, height, "GLFW Test", None, None) #glfw.get_primary_monitor()
    if not window:
        glfw.terminate()
        exit()

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glViewport(0, 0, width, height)

    g = Ground()
