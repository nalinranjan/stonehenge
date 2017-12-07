from OpenGL.GL import *
from OpenGL.GLUT import *
from ground import Ground
from light import Light
from camera import Camera

VERTEX_SHADER = "shader.vert"
FRAGMENT_SHADER = "shader.frag"

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

        self.objects.append(ground)

        glutDisplayFunc(self.display)
        glutIdleFunc(self.display)
        # glutKeyboardFunc(self.keyPressed)

        glutMainLoop()

    @staticmethod
    def init_glut():
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DOUBLE | GLUT_DEPTH
                            | GLUT_3_2_CORE_PROFILE)
        glutInitWindowSize(512, 512)
        glutCreateWindow(b"Final Project - Stonehenge")

        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 0.0)
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

if __name__ == "__main__":
    Scene()
