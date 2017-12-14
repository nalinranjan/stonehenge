"""
scene.py

The driver program. Sets up the scene and its components and displays it.
"""

import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from light import Light
from camera import Camera
from ground import Ground
from stone import Stone
from boulder import Boulder

GROUND_VERTEX_SHADER = "ground_shader.vert"
GROUND_FRAGMENT_SHADER = "ground_shader.frag"
STONE_VERTEX_SHADER = "stone_shader.vert"
STONE_FRAGMENT_SHADER = "stone_shader.frag"

GROUND_SIZE = 20.0

class Scene(object):
    """
    A class encapsulating the entire scene. Contains methods to initialize the
    OpenGL context, setup the camera and lighting, setup the shaders and the
    components of the scene. Displays the scene and handles user input.
    """
    light = None
    camera = None
    ground_shader_program = None
    stone_shader_program = None

    objects = []

    def __init__(self):
        """
        Constructor. Executes the entire 3D pipeline.
        """
        self.init_glut()

        self.light = Light()
        self.camera = Camera()

        self.setup_shaders()

        ground = Ground(self.ground_shader_program)
        ground.scale(GROUND_SIZE, 1.0, GROUND_SIZE)
        self.objects.append(ground)

        self.setup_stones()
        self.setup_boulders()

        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.handle_key)

        glutMainLoop()

    @staticmethod
    def init_glut():
        """
        Sets up the OpenGL context using GLUT.
        """
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DOUBLE | GLUT_DEPTH
                            | GLUT_3_2_CORE_PROFILE)
        glutInitWindowSize(768, 768)
        glutCreateWindow(b"Final Project - Stonehenge")

        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.2, 0.2, 1.0)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClearDepth(1.0)

    def setup_shaders(self):
        """
        Compiles vertex and fragment shaders and links them to shader programs
        used in the scene. Two sets of shaders are used - one for the ground
        and one for the stones.
        """
        vertex_shader = self.compile_shader(GL_VERTEX_SHADER, GROUND_VERTEX_SHADER)
        fragment_shader = self.compile_shader(GL_FRAGMENT_SHADER, GROUND_FRAGMENT_SHADER)
        self.ground_shader_program = self.linkProgram(vertex_shader, fragment_shader)

        vertex_shader = self.compile_shader(GL_VERTEX_SHADER, STONE_VERTEX_SHADER)
        fragment_shader = self.compile_shader(GL_FRAGMENT_SHADER, STONE_FRAGMENT_SHADER)
        self.stone_shader_program = self.linkProgram(vertex_shader, fragment_shader)

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    @staticmethod
    def compile_shader(shader_type, source_path):
        """
        Compiles a shader from a given source file and returns a unique ID
        representing it.

        :param shader_type: The type of shader
        :param source_path: The path of the shader source file

        :return: A unique ID representing the compiled shader
        """
        with open(source_path) as shader_file:
            source = shader_file.read()
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        log = glGetShaderInfoLog(shader)
        if log:
            print(log)
        return shader

    @staticmethod
    def linkProgram(vertex_shader, fragment_shader):
        """
        Creates and returns a shader program after linking a vertex and
        fragment shader to it.

        :param vertex_shader: A unique ID representing the vertex shader
        :param fragment_shader: A unique ID representing the fragment shader

        :return: A unique ID representing the shader program
        """
        shader_program = glCreateProgram()
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)
        log = glGetProgramInfoLog(shader_program)
        if log:
            print(log)
        return shader_program

    def setup_stones(self):
        """
        Creates objects for the gray stones that make up Stonehenge and applies
        model transforms to them.
        """
        stone1 = Stone(self.stone_shader_program)
        stone1.scale(1.5, 3.0, 0.7)
        stone1.rotate(0.0, 20.0, 0.0)
        stone1.translate(3.5, 3.0, 8.5)
        self.objects.append(stone1)

        stone2 = Stone(self.stone_shader_program)
        stone2.scale(1.5, 3.0, 0.7)
        stone2.rotate(0.0, 45.0, 0.0)
        stone2.translate(7.8, 3.0, 5.8)
        self.objects.append(stone2)

        stone3 = Stone(self.stone_shader_program)
        stone3.scale(3.5, 0.5, 0.7)
        stone3.rotate(0.0, 32.5, 0.0)
        stone3.translate(5.7, 6.5, 7.2)
        self.objects.append(stone3)

        stone4 = Stone(self.stone_shader_program)
        stone4.scale(1.5, 3.0, 0.7)
        stone4.rotate(0.0, -25.0, 0.0)
        stone4.translate(-4.5, 3.0, 8.2)
        self.objects.append(stone4)

        stone5 = Stone(self.stone_shader_program)
        stone5.scale(1.5, 3.0, 0.7)
        stone5.rotate(0.0, -40.0, 0.0)
        stone5.translate(-8.5, 3.0, 5.7)
        self.objects.append(stone5)

        stone6 = Stone(self.stone_shader_program)
        stone6.scale(1.5, 3.0, 0.7)
        stone6.rotate(0.0, -55.0, 0.0)
        stone6.translate(-11.8, 3.0, 2.0)
        self.objects.append(stone6)

        stone7 = Stone(self.stone_shader_program)
        stone7.scale(2.7, 0.5, 0.7)
        stone7.rotate(0.0, -32.5, 0.0)
        stone7.translate(-6.0, 6.5, 7.4)
        self.objects.append(stone7)

        stone8 = Stone(self.stone_shader_program)
        stone8.scale(2.7, 0.5, 0.7)
        stone8.rotate(0.0, -47.5, 0.0)
        stone8.translate(-10.5, 6.5, 3.7)
        self.objects.append(stone8)

        stone9 = Stone(self.stone_shader_program)
        stone9.scale(1.5, 3.2, 0.7)
        stone9.rotate(0.0, 77.0, 0.0)
        stone9.translate(11.5, 3.2, 0.8)
        self.objects.append(stone9)

        stone10 = Stone(self.stone_shader_program)
        stone10.scale(2.2, 4.0, 1.0)
        stone10.rotate(0.0, 3.0, 0.0)
        stone10.translate(-3.0, 4.0, -6.0)
        self.objects.append(stone10)

        stone11 = Stone(self.stone_shader_program)
        stone11.scale(2.2, 4.0, 1.0)
        stone11.rotate(0.0, -3.0, 0.0)
        stone11.translate(3.0, 4.0, -6.0)
        self.objects.append(stone11)

        stone12 = Stone(self.stone_shader_program)
        stone12.scale(5.5, 0.6, 0.9)
        stone12.rotate(0.0, 0.0, 0.0)
        stone12.translate(0.0, 8.6, -6.0)
        self.objects.append(stone12)

    def setup_boulders(self):
        """
        Creates objects for the boulders present along Stonehenge and applies
        model transforms to them.
        """
        boulder1 = Boulder(self.stone_shader_program)
        boulder1.scale(1.0, 1.0, 1.0)
        boulder1.translate(10.0, -0.2, -7.5)
        self.objects.append(boulder1)

        boulder2 = Boulder(self.stone_shader_program)
        boulder2.scale(1.3, 1.3, 1.3)
        boulder2.translate(8.0, -0.4, -9.0)
        self.objects.append(boulder2)

        boulder3 = Boulder(self.stone_shader_program)
        boulder3.scale(2.0, 2.0, 2.0)
        boulder3.translate(-0.8, -1.0, 1.3)
        self.objects.append(boulder3)

        boulder4 = Boulder(self.stone_shader_program)
        boulder4.scale(1.7, 1.7, 1.7)
        boulder4.translate(-4.1, -0.8, 0.1)
        self.objects.append(boulder4)

        boulder5 = Boulder(self.stone_shader_program)
        boulder5.scale(1.3, 1.3, 1.3)
        boulder5.translate(2.8, -0.5, 0.5)
        self.objects.append(boulder5)

    def display(self):
        """
        Displays the scene on the current OpenGL window.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set up parameters for the ground
        glUseProgram(self.ground_shader_program)
        self.camera.setup(self.ground_shader_program)
        self.light.setup(self.ground_shader_program)
        self.objects[0].draw(self.ground_shader_program)

        # Set up parameters for the stones and boulders
        glUseProgram(self.stone_shader_program)
        self.camera.setup(self.stone_shader_program)
        self.light.setup(self.stone_shader_program)

        for obj in self.objects[1:]:
            obj.draw(self.stone_shader_program)

        glutSwapBuffers()

    def handle_key(self, *args):
        """
        Handles user input to rotate the scene or quit.

        :param *args: User input parameters passed by GLUT
        """
        key = args[0].decode()

        # Rotate the scene clockwise
        if key == 'a':
            for obj in self.objects:
                obj.rotate(0, 2, 0)

        # Rotate the scene counter-clockwise
        elif key == 'd':
            for obj in self.objects:
                obj.rotate(0, -2, 0)

        # Close the window
        elif key == 'q':
            sys.exit(0)

        self.display()

if __name__ == "__main__":
    Scene()
