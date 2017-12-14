"""
camera.py

Contains the Camera class to manage the view and projection matrices.
"""

import math
import numpy as np
from OpenGL.GL import *

class Camera(object):
    """
    Sets up the view and projection matrices based on camera and frustum
    parameters.
    """
    eyepoint = [0.0, 38.0, 50.0]
    lookat = [0.0, 0.0, 0.0]
    up = [0.0, 1.0, 0.0]

    left, right = -1.0, 1.0
    bottom, top = -1.0, 1.0
    near, far = 3.0, 200.0

    def __init__(self):
        """
        Contructor. Sets up the eyepoint, lookat and up arrays.
        """
        self.eyepoint = np.array([*self.eyepoint], dtype=np.float32)
        self.lookat = np.array([*self.lookat], dtype=np.float32)
        self.up = np.array([*self.up], dtype=np.float32)

    def setup(self, shader_program):
        """
        Sends the view and projection matrices to a given shader program.

        :param shader_program: A unique ID representing the shader program
        """
        self.setup_view(shader_program)
        self.setup_projection(shader_program)

    def setup_view(self, shader_program):
        """
        Calculates the view matrix and passes it to a given shader program.

        :param shader_program: A unique ID representing the shader program
        """
        n = self.normalize(self.eyepoint - self.lookat)
        u = self.normalize(np.cross(self.normalize(self.up), n))
        v = self.normalize(np.cross(n, u))

        view_mat = np.array([u[0], v[0], n[0], 0.0,
                             u[1], v[1], n[1], 0.0,
                             u[2], v[2], n[2], 0.0,
                             -np.dot(u, self.eyepoint),
                             -np.dot(v, self.eyepoint),
                             -np.dot(n, self.eyepoint), 1.0],
                            dtype=np.float32)

        view_location = glGetUniformLocation(shader_program, "view")
        glUseProgram(shader_program)
        glUniformMatrix4fv(view_location, 1, GL_FALSE, view_mat)

    def setup_projection(self, shader_program):
        """
        Calculates the projection matrix and passes it to a given shader program.

        :param shader_program: A unique ID representing the shader program
        """
        projection_mat = np.array([(2.0*self.near)/(self.right-self.left), 0.0, 0.0, 0.0,
                                   0.0, ((2.0*self.near)/(self.top-self.bottom)), 0.0, 0.0,
                                   ((self.right+self.left)/(self.right-self.left)),
                                   ((self.top+self.bottom)/(self.top-self.bottom)),
                                   ((-1.0*(self.far+self.near)) / (self.far-self.near)), -1.0,
                                   0.0, 0.0, ((-2.0*self.far*self.near)/(self.far-self.near)),
                                   0.0], dtype=np.float32)

        projection_location = glGetUniformLocation(shader_program, "projection")
        glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection_mat)

    @staticmethod
    def normalize(vector):
        """
        Returns a given vector in normalized form.

        :param vector: The vector to be normalized
        """
        return vector / np.linalg.norm(vector)
