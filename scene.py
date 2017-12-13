import sys
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from light import Light
from camera import Camera
from ground import Ground
from stone import Stone

GROUND_VERTEX_SHADER = "ground_shader.vert"
GROUND_FRAGMENT_SHADER = "ground_shader.frag"
STONE_VERTEX_SHADER = "stone_shader.vert"
STONE_FRAGMENT_SHADER = "stone_shader.frag"

GROUND_SIZE = 20.0

class Scene(object):
    light = None
    camera = None
    ground_shader_program = None
    stone_shader_program = None

    objects = []

    def __init__(self):
        self.init_glut()

        self.light = Light()
        self.camera = Camera()

        self.setup_shaders()

        ground = Ground(self.ground_shader_program)
        ground.scale(GROUND_SIZE, 1.0, GROUND_SIZE)
        self.objects.append(ground)

        self.setup_stones()

        glutDisplayFunc(self.display)
        glutIdleFunc(self.display)
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
        # glViewport(0, 0, 768, 768)
        glEnable(GL_CULL_FACE)
        # glFrontFace(GL_CCW)
        glCullFace(GL_BACK)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClearDepth(1.0)

    def setup_shaders(self):
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
        shader_program = glCreateProgram()
        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)
        log = glGetProgramInfoLog(shader_program)
        if log:
            print(log)
        return shader_program

    def setup_stones(self):
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

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.ground_shader_program)
        self.camera.setup(self.ground_shader_program)
        self.light.setup(self.ground_shader_program)
        self.objects[0].draw(self.ground_shader_program)

        glUseProgram(self.stone_shader_program)
        self.camera.setup(self.stone_shader_program)
        self.light.setup(self.stone_shader_program)

        for obj in self.objects[1:]:
            obj.draw(self.stone_shader_program)

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
        
        # self.camera.setup_view(self.shader_program)
        self.display()


if __name__ == "__main__":
    Scene()
