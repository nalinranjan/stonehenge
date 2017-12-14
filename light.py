import numpy as np
from OpenGL.GL import *

class Light(object):
    position = [-20.0, 20.0, -50.0]
    ambient = [1.0, 0.9, 0.9]
    diffuse = [1.0, 0.9, 0.9]
    specular = [1.0, 1.0, 1.0]

    def __init__(self):
        self.position = np.array([*self.position], dtype=np.float32)
        self.ambient = np.array([*self.ambient], dtype=np.float32)
        self.diffuse = np.array([*self.diffuse], dtype=np.float32)
        self.specular = np.array([*self.specular], dtype=np.float32)

    def setup(self, shader_program):
        position_location = glGetUniformLocation(shader_program, "lightPosition")
        ambient_location = glGetUniformLocation(shader_program, "I_a")
        diffuse_location = glGetUniformLocation(shader_program, "I_d")
        specular_location = glGetUniformLocation(shader_program, "I_s")

        glUseProgram(shader_program)
        glUniform3fv(position_location, 1, self.position)
        glUniform3fv(ambient_location, 1, self.ambient)
        glUniform3fv(diffuse_location, 1, self.diffuse)
        glUniform3fv(specular_location, 1, self.specular)
