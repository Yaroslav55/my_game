import sys
from ctypes import c_void_p

from OpenGL.GL import glFlush
from OpenGL.GL import glShaderSource, glGetShaderiv, glGenVertexArrays, glGenBuffers, glBufferData, \
    glVertexAttribPointer, glGenTextures, glTexImage2D, glDrawElements
from OpenGL.GL.framebufferobjects import glGenerateMipmap
from OpenGL.GL.shaders import glAttachShader, GL_LINK_STATUS, glGetProgramInfoLog, glGetProgramiv, glDeleteShader, \
    GL_FALSE
from OpenGL.GLUT import glutInitContextVersion, glutInit, glutCreateWindow, glutDisplayFunc, glutSpecialFunc, \
    glutReshapeFunc, glutTimerFunc
from OpenGL.arrays._arrayconstants import GL_UNSIGNED_BYTE, GL_UNSIGNED_INT
from OpenGL.raw.GL.ARB.robustness import GL_NO_ERROR
from OpenGL.raw.GL.ARB.vertex_array_object import glBindVertexArray
from OpenGL.raw.GL.ARB.vertex_shader import GL_FLOAT
from OpenGL.raw.GL.VERSION.GL_1_0 import glGetError, GL_TEXTURE_2D, glPixelStorei, GL_RGB, GL_RGBA, GL_UNPACK_ALIGNMENT, \
    glTexParameterf, GL_TEXTURE_ENV_MODE, GL_TEXTURE_MIN_FILTER, GL_NEAREST, GL_TEXTURE_MAG_FILTER, glTexEnvf, \
    GL_TEXTURE_ENV, GL_DECAL, glEnable, glViewport, glMatrixMode, glLoadIdentity, GL_PROJECTION, GL_MODELVIEW, \
    glFrustum, GL_TRIANGLES, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glClear, glClearColor, glScalef, GL_DEPTH_TEST, \
    glPolygonMode, GL_FRONT_AND_BACK, GL_FILL, \
    glLineWidth, GL_LINE
from OpenGL.raw.GL.VERSION.GL_1_1 import glBindTexture
from OpenGL.raw.GL.VERSION.GL_1_5 import glBindBuffer, GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW
from OpenGL.raw.GL.VERSION.GL_2_0 import GL_VERTEX_SHADER, GL_COMPILE_STATUS, glCompileShader, glGetShaderInfoLog, \
    glCreateShader, GL_FRAGMENT_SHADER, glCreateProgram, glLinkProgram, glUseProgram, glEnableVertexAttribArray
from OpenGL.raw.GLU import gluErrorString, gluLookAt
from OpenGL.raw.GLUT import GLUT_KEY_PAGE_DOWN, GLUT_KEY_END, GLUT_KEY_HOME, GLUT_KEY_PAGE_UP, GLUT_KEY_RIGHT, \
    GLUT_KEY_LEFT, GLUT_KEY_DOWN, \
    GLUT_KEY_UP, glutInitDisplayMode, glutInitWindowSize, GLUT_SINGLE, GLUT_RGB, glutInitWindowPosition, glutMainLoop, \
    glutPostRedisplay
from PIL import Image

from typing import Union
from typing import List

from backend.debug_logger import Logger
from backend.entities.entities import Mesh
from backend.graphic_engine.engine_abstract import Graphic
from camera import Camera3D
from model_loader import Model
from scene import Scene, Vector3f


class OpenGLRender(Graphic):
    _GAME_TIMER = 15  # Related to game FPS
    GAME_MODE = "3D"

    def __init__(self, camera_obj: Camera3D, scene: Scene, upd_func):
        self._camera_obj = camera_obj
        self._game_scene = scene
        self._update_func = upd_func
        self.default_vertexShaderSource = """
                    #version 330 compatibility
                    varying vec4 aPos;
                    void main()
                    {
                        gl_TexCoord[0]=gl_MultiTexCoord0;
                        aPos = gl_Vertex;
                        //gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                        gl_Position = gl_ModelViewProjectionMatrix * aPos;
                    }
                    """
        self.default_fragmentShaderSource = """
                    #version 330 compatibility
                    uniform sampler2D ourTexture;
                    void main(void) {
                        vec4 textureForPixel = texture2D(ourTexture, gl_TexCoord[0].st );

                        gl_FragColor = textureForPixel;

                    }
                    """
        self.vertexShaderSource = """
                    #version 330 compatibility
                    layout (location = 0) in vec3 aPos;
                    layout (location = 1) in vec3 aColor;
                    layout (location = 2) in vec2 aTexCoord;
                    out vec3 ourColor;
                    out vec2 TexCoord;
                    void main()
                    {
                        gl_Position = gl_ModelViewProjectionMatrix * vec4(aPos, 1.0);
                        ourColor = aColor;
                        TexCoord = aTexCoord;
                    }"""
        self.fragmentShaderSource = """
                    #version 330 core
                    in vec3 ourColor;
                    in vec2 TexCoord;
                    out vec4 FragColor;
                    uniform sampler2D ourTexture;
                        void main()
                        {
                            FragColor = texture(ourTexture, TexCoord);
                            //FragColor = ourColor;
                        }
                    """
        self.shaderProgram = None

    def run(self):
        self._opengl_init()

    def _load_Meshes_in_VAO(self, meshes : list[Mesh] | Mesh):
        float_size = 4  # min size of element in one vertex
        vertex_size = 8  # numb value for one vertex
        def load_mesh(mesh: Mesh):
            vertices = mesh.model_data
            indices = mesh.vertex_indices


            # bind the  Vertex Array Object first, then bind and set vertex  buffer(s), and then configure        vertex        attributes(s).
            mesh.VAO = glGenVertexArrays(1)
            glBindVertexArray(mesh.VAO)

            # Set vertices in VBO
            mesh.VBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, mesh.VBO)
            glBufferData(GL_ARRAY_BUFFER, vertices.size * float_size, vertices, GL_STATIC_DRAW)

            # Set vertex index
            mesh.EBO = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.EBO)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * float_size, indices, GL_STATIC_DRAW)

            # position  attribute
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertex_size * vertices.itemsize, None)
            glEnableVertexAttribArray(0)
            # color     attribute
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertex_size * vertices.itemsize, c_void_p(3 * float_size))
            glEnableVertexAttribArray(1)
            # textures coord
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, vertex_size * vertices.itemsize, c_void_p(6 * float_size))
            glEnableVertexAttribArray(2)

            # # Развязка VBO и EBO
            # glBindBuffer(GL_ARRAY_BUFFER, 0)
            # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
            #
            # # Развязка VAO
            # glBindVertexArray(0)
            #
            # load mesh textures
            mesh.material = self.load_textures(mesh.texture_name)

        if isinstance(meshes, Mesh):
            load_mesh(meshes)
        else:
            for mesh in meshes:
                load_mesh(mesh)

        return 0

    def set_shaders(self, vertexShader_source, fragmentShaderSource):
        def compileShader(type, shader_source):
            shader = glCreateShader(type)
            glShaderSource(shader, shader_source)
            glCompileShader(shader)
            return shader

        vertexShader = compileShader(GL_VERTEX_SHADER, vertexShader_source)
        success = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)
        if not success:
            info_mesg = glGetShaderInfoLog(vertexShader)
            Logger.err(f"ERROR::SHADER::VERTEX::COMPILATION_FAILED {info_mesg}",)
            return -1
        # fragment        shader
        fragmentShader = compileShader(GL_FRAGMENT_SHADER, fragmentShaderSource)
        # check for shader compile errors
        success = glGetShaderiv(fragmentShader, GL_COMPILE_STATUS)
        if not success:
            info_mesg = glGetShaderInfoLog(fragmentShader)
            Logger.err(f"ERROR::SHADER::FRAGMENT::COMPILATION_FAILED {info_mesg}")
            return -1
        # link        shaders
        self.shaderProgram = glCreateProgram()
        glAttachShader(self.shaderProgram, vertexShader)
        glAttachShader(self.shaderProgram, fragmentShader)
        glLinkProgram(self.shaderProgram)
        # check for linking errors
        success = glGetProgramiv(self.shaderProgram, GL_LINK_STATUS)
        if not success:
            info_mesg = glGetProgramInfoLog(self.shaderProgram)
            Logger.err(f"ERROR::SHADER::PROGRAM::LINKING_FAILED {info_mesg}")
            return -1
        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)
        glUseProgram(self.shaderProgram)
        return 0

    def update_meshes_in_memory(self):
        for model in self._game_scene.models:
            if model.need_update_mesh:
                self._load_Meshes_in_VAO(self._game_scene.models)
                model.need_update_mesh = False
                # model.clear_model_data()

    def _load_meshes_in_v_memory(self):
        self.set_shaders(self.vertexShaderSource, self.fragmentShaderSource)
        self._load_Meshes_in_VAO(self._camera_obj.player_mesh)
        self.update_meshes_in_memory()

    def _opengl_init(self):
        glutInitContextVersion(3, 1)
        # glutInitContextFlags(GLUT_FORWARD_COMPATIBLE)
        # glutInitContextProfile(GLUT_CORE_PROFILE)

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(b"Transformed Cube")
        # Old init func
        self._load_meshes_in_v_memory()
        # print(float(glGetString(GL_VERSION)[:3]))

        # glShadeModel(GL_FLAT)
        # -------
        glutDisplayFunc(self.display)
        glutSpecialFunc(self.Keyboard)
        glutReshapeFunc(self.reshape)
        glutTimerFunc(self._GAME_TIMER, self.update_frame, 0)
        glutMainLoop()

    def update_frame(self, value):
        """
            The main method for rerender screen
        """
        self.opengl_error_check()
        self._update_func()
        glutPostRedisplay()
        glutTimerFunc(self._GAME_TIMER, self.update_frame, 0)

    def reshape(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-0.5, 0.5, -1.0, 1.0, 1.5, 6050.0)
        glMatrixMode(GL_MODELVIEW)

    def _make_camera(self, pos: Union[Vector3f, List[float]], look: Union[Vector3f, List[float]]):

        gluLookAt(pos[0], pos[1], pos[2], look[0], look[1], look[2], 0.0, 1.0, 0.0)
        self._draw_meshes_with_vao(self._camera_obj.player_mesh)

    def _load_texture(self, texture_name) -> Image:
        try:
            im = Image.open(texture_name)
            convert = im.convert("RGBA")
        except OSError:
            Logger.warn(f"Cannot open img {texture_name}")
            return -1
        return convert

    def load_textures(self, tex_name: str):
        texture_img = self._load_texture(tex_name)
        if not texture_img:
            Logger.warn("texture_img is absent!")
            return -1

        texture_ptr = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_ptr)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_img.width, texture_img.height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, texture_img.tobytes())
        glGenerateMipmap(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        return texture_ptr

    def drawCube(self):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 288, 288,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, self._load_texture("test_img.jpg"))
        glGenerateMipmap(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    def _draw_meshes_with_vao(self, meshes: list[Mesh]):
        def draw(VAO_obj):
            # glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, VAO_obj.material)
            glBindVertexArray(VAO_obj.VAO)
            glDrawElements(GL_TRIANGLES, len(VAO_obj.vertex_indices), GL_UNSIGNED_INT, None)
            glBindVertexArray(0)
            # glDrawArrays(GL_TRIANGLE_STRIP, 0, 6)

        if isinstance(meshes, Model):
            draw(meshes)
        else:
            for mesh in meshes:
                draw(mesh)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glLoadIdentity()
        # glColor3f(1.0, 1.0, 1.0)
        glScalef(1.0, 2.0, 1.0)
        self._make_camera(self._camera_obj.get_postion(), self._camera_obj.get_point_of_view())
        self._draw_meshes_with_vao(self._game_scene.models)
        glEnable(GL_DEPTH_TEST)
        if 0:
            glLineWidth(1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        # glutSolidCube(0.05)
        glFlush()

    def opengl_error_check(self):
        error = glGetError()
        if error != GL_NO_ERROR:
            Logger.wanr(f"OPENGL_ERROR: {gluErrorString(error)}")

    def INfutureForDestrustor(self):
        # Опционально: освобождаем        все        ресурсы, как        только
        #  они        выполнили        свое        предназначение
        # glDeleteVertexArrays(1, & VAO);
        # glDeleteBuffers(1, & VBO);
        # glDeleteBuffers(1, & EBO);
        pass

    def Keyboard(self, key, x, y):
        rotate_angle = self._camera_obj.CAMERA_ANGEL

        if key == GLUT_KEY_UP:  # Клавиша вверх
            self._camera_obj.move_forward()
        elif key == GLUT_KEY_DOWN:  # Клавиша вниз
            self._camera_obj.move_back()
        elif key == GLUT_KEY_LEFT:  # Клавиша влево
            self._camera_obj.move_left()
        elif key == GLUT_KEY_RIGHT:  # Клавиша вправо
            self._camera_obj.move_right()
        elif key == GLUT_KEY_PAGE_UP:  # Клавиша вниз
            self._camera_obj.rotate_Y(rotate_angle)
        elif key == GLUT_KEY_HOME:  # Клавиша вниз Y
            self._camera_obj.move_up()
        elif key == GLUT_KEY_END:
            self._camera_obj.move_down()
        elif key == GLUT_KEY_PAGE_DOWN:  # Клавиша вниз
            self._camera_obj.rotate_Y(-rotate_angle)
