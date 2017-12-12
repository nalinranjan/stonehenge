import sys
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from light import Light
from camera import Camera
from ground import Ground
from stone import Stone

VERTEX_SHADER = "shader.vert"
FRAGMENT_SHADER = "shader.frag"

GROUND_SIZE = 20.0

class Scene(object):
    light = None
    camera = None
    shader_program = None

    objects = []

    def __init__(self):
        self.init_glut()

        self.light = Light()
        self.camera = Camera()

        self.setup_shaders()

        self.light.setup(self.shader_program)
        self.camera.setup(self.shader_program)

        ground = Ground()
        ground.scale(GROUND_SIZE, 1.0, GROUND_SIZE)
        # ground.translate(0.0, 0.0, GROUND_SIZE)
        self.objects.append(ground)

        # stone1 = Stone()
        # stone1.scale(2.0, 3.0, 1.0)
        # stone1.translate(0.0, 5.0, 0.0)
        # self.objects.append(stone1)

        # stone2 = Stone()
        # stone2.scale(2.0, 3.0, 1.0)
        # stone2.translate(8.0, 3.0, 2.0)
        # self.objects.append(stone2)

        glutDisplayFunc(self.display)
        # glutIdleFunc(self.display)
        glutKeyboardFunc(self.handle_key)

        glutMainLoop()

    @staticmethod
    def init_glut():
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DOUBLE | GLUT_DEPTH
                            | GLUT_3_2_CORE_PROFILE)
        glutInitWindowSize(768, 768)
        glutCreateWindow(b"Final Project - Stonehenge")

        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.2, 0.2, 1.0)
        glViewport(0, 0, 768, 768)
        glEnable(GL_CULL_FACE)
        # glFrontFace(GL_CCW)
        glCullFace(GL_BACK)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClearDepth(1.0)

    def setup_shaders(self):
        vertex_shader = self.compile_shader(GL_VERTEX_SHADER, VERTEX_SHADER)
        fragment_shader = self.compile_shader(GL_FRAGMENT_SHADER, FRAGMENT_SHADER)

        self.shader_program = glCreateProgram()
        glAttachShader(self.shader_program, vertex_shader)
        glAttachShader(self.shader_program, fragment_shader)
        glLinkProgram(self.shader_program)
        log = glGetProgramInfoLog(self.shader_program)
        if log:
            print(log)

    @staticmethod
    def compile_shader(shader_type, source_path):
        with open(source_path) as shader_file:
            source = shader_file.read()
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        log = glGetShaderInfoLog(shader)
        if log:
            print(log)
        return shader

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for obj in self.objects:
            obj.draw(self.shader_program)
        
        glutSwapBuffers()

    def handle_key(self, *args):
        key = args[0].decode()
        if key == 'a':
            for obj in self.objects:
                obj.rotate(0, 2, 0)
            # self.camera.rotate(-2)
        elif key == 'd':
            for obj in self.objects:
                obj.rotate(0, -2, 0)
            # self.camera.rotate(2)
        elif key == 'q':
            sys.exit(0)
        
        self.display()
        # self.camera.setup_view(self.shader_program)


if __name__ == "__main__":
    Scene()
