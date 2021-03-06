"""
object.py

Contains the base class SceneObject from which all objects making up the
scene are derived.
"""

import math
import numpy as np
from OpenGL.GL import *
from pysoil import *
from ctypes import c_void_p

class SceneObject(object):
    """
    Represents an object in the scene. Contains methods to load textures,
    buffer data to the GPU, perform model transforms and render the object.
    """
    vertices = np.array([], dtype=np.float32)
    elements = np.array([], dtype=np.float32)
    normals = np.array([], dtype=np.float32)
    texture_uv = np.array([], dtype=np.float32)
    transform = np.identity(4, dtype=np.float32)

    texture = 0
    vao = GLuint(0)

    k_ambient = np.array([], dtype=np.float32)
    k_diffuse = np.array([], dtype=np.float32)
    k_specular = np.array([], dtype=np.float32)
    shininess = 0.0

    def load_texture(self, texture_path):
        """
        Creates a texture from an image.

        :param texture_path: The path of the texture image.
        """
        try:
            self.texture = SOIL_load_OGL_texture(
                texture_path,
                SOIL_LOAD_AUTO,
                SOIL_CREATE_NEW_ID,
                SOIL_FLAG_INVERT_Y | SOIL_FLAG_TEXTURE_REPEATS
            )

        except Exception as soil_ex:
            print('SOIL_load_OGL_texture ERROR', soil_ex)

    def set_buffers(self, shader_program):
        """
        Buffers the vertex, element, normal and texture data to the GPU.

        :param shader_program: A unique ID for the shader_program to be used
                               with this object
        """
        # Generate a Vertex Array Object
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Generate buffers for elements and vertices
        buffer_objects = glGenBuffers(2)

        # Buffer element data
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer_objects[0])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.elements, GL_STATIC_DRAW)

        # Buffer vertex data (position, normal and texture)
        glBindBuffer(GL_ARRAY_BUFFER, buffer_objects[1])
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes + self.normals.nbytes
                     + (self.texture_uv.nbytes if self.texture > 0 else 0),
                     None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0,
                        self.vertices.nbytes, self.vertices)
        glBufferSubData(GL_ARRAY_BUFFER, self.vertices.nbytes,
                        self.normals.nbytes, self.normals)
        if self.texture > 0:
            glBufferSubData(GL_ARRAY_BUFFER, self.vertices.nbytes + self.normals.nbytes,
                            self.texture_uv.nbytes, self.texture_uv)

        glUseProgram(shader_program)

        # Set attribute pointers in the shader program
        vertex_location = glGetAttribLocation(shader_program, "vPosition")
        normal_location = glGetAttribLocation(shader_program, "vNormal")

        glVertexAttribPointer(vertex_location, 3, GL_FLOAT, GL_FALSE, 0,
                              c_void_p(0))
        glVertexAttribPointer(normal_location, 3, GL_FLOAT, GL_FALSE, 0,
                              c_void_p(self.vertices.nbytes))

        glEnableVertexAttribArray(vertex_location)
        glEnableVertexAttribArray(normal_location)

        if self.texture > 0:
            texture_location = glGetAttribLocation(shader_program, "vTexCoords")
            glVertexAttribPointer(texture_location, 2, GL_FLOAT, GL_FALSE, 0,
                                  c_void_p(self.vertices.nbytes + self.normals.nbytes))
            glEnableVertexAttribArray(texture_location)

        # Unbind the buffer objects
        glBindVertexArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, shader_program):
        """
        Sends the required parameters to the vertex shader and renders the
        shape.

        :param shader_program: A unique ID for the shader_program to be used
        """
        glUseProgram(shader_program)
        glBindVertexArray(self.vao)

        # Pass the model matrix to the shader
        model_location = glGetUniformLocation(shader_program, "model")
        glUniformMatrix4fv(model_location, 1, GL_FALSE,
                           self.transform.transpose().reshape((1, 16)))

        # Pass the material properties to the shader
        ambient_location = glGetUniformLocation(shader_program, "k_a")
        diffuse_location = glGetUniformLocation(shader_program, "k_d")
        specular_location = glGetUniformLocation(shader_program, "k_s")
        shininess_location = glGetUniformLocation(shader_program, "n")

        glUniform3fv(ambient_location, 1, self.k_ambient)
        glUniform3fv(diffuse_location, 1, self.k_diffuse)
        glUniform3fv(specular_location, 1, self.k_specular)
        glUniform1f(shininess_location, self.shininess)

        # Pass texture data to the sampler if the object has a texure
        if self.texture > 0:
            glActiveTexture(GL_TEXTURE0 + self.texture)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            tex_sampler_location = glGetUniformLocation(shader_program, "tex")
            glUniform1i(tex_sampler_location, self.texture)

        # Render the object
        glDrawElements(GL_TRIANGLES, len(self.elements), GL_UNSIGNED_SHORT, None)

        glBindVertexArray(0)

    def scale(self, x, y, z):
        """
        Modifies the current model transform to scale the object.

        :param x: The scale value in the x-direction
        :param y: The scale value in the y-direction
        :param z: The scale value in the z-direction
        """
        scale_mat = np.array([[x, 0.0, 0.0, 0.0],
                              [0.0, y, 0.0, 0.0],
                              [0.0, 0.0, z, 0.0],
                              [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)
        self.transform = scale_mat @ self.transform

    def rotate(self, x, y, z):
        """
        Modifies the current model transform to rotate the object. The order of
        rotation is y -> z -> x.

        :param x: The rotation angle (in degrees) in the x-direction
        :param y: The rotation angle (in degrees) in the y-direction
        :param z: The rotation angle (in degrees) in the z-direction
        """
        x = math.radians(x)
        y = math.radians(y)
        z = math.radians(z)

        cos_x, sin_x = math.cos(x), math.sin(x)
        cos_y, sin_y = math.cos(y), math.sin(y)
        cos_z, sin_z = math.cos(z), math.sin(z)

        x_mat = np.array([[1.0, 0.0, 0.0, 0.0],
                          [0.0, cos_x, -sin_x, 0.0],
                          [0.0, sin_x, cos_x, 0.0],
                          [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)

        y_mat = np.array([[cos_y, 0.0, sin_y, 0.0],
                          [0.0, 1.0, 0.0, 0.0],
                          [-sin_y, 0.0, cos_y, 0.0],
                          [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)

        z_mat = np.array([[cos_z, -sin_z, 0.0, 0.0],
                          [sin_z, cos_z, 0.0, 0.0],
                          [0.0, 0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)

        # Order of rotation: y -> z -> x
        self.transform = x_mat @ z_mat @ y_mat @ self.transform

    def translate(self, x, y, z):
        """
        Modifies the current model transform to translate the object.

        :param x: The translation value in the x-direction
        :param y: The translation value in the y-direction
        :param z: The translation value in the z-direction
        """
        translate_mat = np.array([[1.0, 0.0, 0.0, x],
                                  [0.0, 1.0, 0.0, y],
                                  [0.0, 0.0, 1.0, z],
                                  [0.0, 0.0, 0.0, 1.0]], dtype=np.float32)
        self.transform = translate_mat @ self.transform
