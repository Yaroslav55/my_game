from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

import time
import numpy as np
from typing import Union
from typing import List

from camera import Camera
from scene import Scene, Vector3f
import const_variables_store as const_var


class Render(object):
    _GAME_TIMER = 15  # Related to game FPS
    GAME_MODE = "3D"

    def __init__(self, camera_obj: Camera, scene: Scene, upd_func):
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

    def _load_Chunks_in_VAO(self):
        float_size = 4  # min size of element in one vertex
        for cur_chunk in self._game_scene.chunks:
            vertices = cur_chunk.vertex_array
            indices = np.array((cur_chunk.index_array), dtype=np.int32)
            cur_chunk.VAO = glGenVertexArrays(1)
            cur_chunk.VBO = glGenBuffers(1)
            cur_chunk.EBO = glGenBuffers(1)
            # bind the  Vertex Array Object first, then bind and set vertex  buffer(s), and then configure        vertex        attributes(s).
            glBindVertexArray(cur_chunk.VAO)
            # Set vertices in VBO
            glBindBuffer(GL_ARRAY_BUFFER, cur_chunk.VBO)
            glBufferData(GL_ARRAY_BUFFER, vertices.size * float_size, vertices, GL_STATIC_DRAW)
            # Set vertex index
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cur_chunk.EBO)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4, indices, GL_STATIC_DRAW)

            # mPosition = glGetAttribLocation(self.shaderProgram, "aPos") # Or 0
            # position  attribute
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 8 * float_size, None)
            glEnableVertexAttribArray(0)
            # color     attribute
            glVertexAttribPointer(1, 3, GL_FLOAT, False, 8 * float_size, c_void_p(3 * float_size))
            glEnableVertexAttribArray(1)
            # textures coord
            glVertexAttribPointer(2, 2, GL_FLOAT, False, 8 * float_size, c_void_p(6 * float_size))
            glEnableVertexAttribArray(2)
            # load mesh textures
            self.load_textures(cur_chunk.material, cur_chunk.texture_name)

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
            print("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n", info_mesg)
            return -1
        # fragment        shader
        fragmentShader = compileShader(GL_FRAGMENT_SHADER, fragmentShaderSource)
        # check for shader compile errors
        success = glGetShaderiv(fragmentShader, GL_COMPILE_STATUS)
        if not success:
            info_mesg = glGetShaderInfoLog(fragmentShader)
            print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n", info_mesg)
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
            print("ERROR::SHADER::PROGRAM::LINKING_FAILED\n", info_mesg)
            return -1
        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)
        glUseProgram(self.shaderProgram)
        return 0

    def _opengl_init(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(100, 100)
        glutCreateWindow("Transformed Cube")
        # Old init func
        self.set_shaders(self.vertexShaderSource, self.fragmentShaderSource)
        self._load_Chunks_in_VAO()
        # print(float(glGetString(GL_VERSION)[:3]))

        # glShadeModel(GL_FLAT)
        # -------
        glutDisplayFunc(self.display)
        glutSpecialFunc(self.Keyboard)
        glutReshapeFunc(self.reshape)
        glutTimerFunc(self._GAME_TIMER, self.update_frame, 0)
        glutMainLoop()

    def update_frame(self, value):

        self.opengl_error_check()
        self._update_func()
        glutPostRedisplay()
        glutTimerFunc(self._GAME_TIMER, self.update_frame, 0)

    def make_line(self, start_pos: Vector3f, end_pos: Vector3f, color: Vector3f):
        glColor3f(color.x, color.y, color.z)  # Grid color
        glBegin(GL_LINES)
        glVertex3f(start_pos.x, start_pos.y, start_pos.z)
        glVertex3f(end_pos.x, end_pos.y, end_pos.z)
        glEnd()

    def _draw_lines(self):
        #       Draw all lines on the scene
        glBegin(GL_LINES)
        glColor3d(1, 1, 0)
        for i in range(300)[::2]:
            _pos_start = self._game_scene.lines_aray[i]
            _pos_end = self._game_scene.lines_aray[i + 1]
            glVertex3d(_pos_start.x, _pos_start.y, _pos_start.z)
            glVertex3d(_pos_end.x, _pos_end.y, _pos_end.z)
        glEnd()

    def _draw_terrain(self, line_mode: bool = 0):
        texture = None
        self.load_textures(texture ,"test_number.jpg")
        #glBindTexture(GL_TEXTURE_2D, texture)
        #       Draw game terrain
        for index, chunk in enumerate(self._game_scene.chunks):
            start_index = 0
            last_index = int(start_index + (chunk.numb_of_faces * chunk.numb_of_faces) * 2 - 1)
            glBegin(GL_TRIANGLE_STRIP)
            for i in chunk.index_array[start_index:last_index]:
                try:
                    pos = Vector3f(chunk.vertex_array[i][0], chunk.vertex_array[i][1],
                                   chunk.vertex_array[i][2])
                    color = Vector3f(chunk.vertex_array[i][3], chunk.vertex_array[i][4],
                                     chunk.vertex_array[i][5])
                    text_coord = Vector3f(chunk.vertex_array[i][6], chunk.vertex_array[i][7],
                                     0)
                    glColor3f(color.x, color.y, color.z)
                    glTexCoord2f(text_coord.x, text_coord.y);
                    glVertex3d(pos.x, pos.y, pos.z)

                except IndexError:
                    print("Error: Triangle index dont have a vertex pair: index ", i - 1)
            glEnd()
        #       -------------

    def reshape(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-0.5, 0.5, -1.0, 1.0, 1.5, 100.0)
        glMatrixMode(GL_MODELVIEW);

    def _make_camera(self, pos: Union[Vector3f, List[float]], look: Union[Vector3f, List[float]]):

        if self.GAME_MODE == "3D":
            gluLookAt(pos[0], pos[1], pos[2], look[0], look[1], look[2], 0.0, 1.0, 0.0)
        elif self.GAME_MODE == "2D":
            pass

    def _load_texture(self, texture_name) -> Image:
        try:
            im = Image.open(texture_name)
            convert = im.convert("RGBA")
        except OSError:
            print("Cannot open img ", texture_name)
            return -1
        return convert

    def load_textures(self, texture_ptr, name):
        texture_img = self._load_texture(name)
        if not texture_img:
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

        glBindTexture(GL_TEXTURE_2D, texture_ptr)

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
        # glVertexPointer(3, GL_FLOAT, 0, None)
        # """Draw a cube with texture coordinates"""
        # texcoord_index = glGetAttribLocation(self.shaderProgram, "in_coord");
        # glBegin(GL_QUADS);
        # glTexCoord2f(0.0, 0.0);
        # glVertex3f(-1.0, -1.0, 1.0);
        # glTexCoord2f(1.0, 0.0);
        #
        # glVertex3f(1.0, -1.0, 1.0);
        # glTexCoord2f(1.0, 1.0);
        #
        # glVertex3f(1.0, 1.0, 1.0);
        #
        # glTexCoord2f(0.0, 1.0);
        # glVertex3f(-1.0, 1.0, 1.0);
        # glTexCoord2f(1.0, 0.0);
        # glVertex3f(-1.0, -1.0, -1.0);
        #
        # glTexCoord2f(1.0, 1.0);
        # glVertex3f(-1.0, 1.0, -1.0);
        #
        # glTexCoord2f(0.0, 1.0);
        # glVertex3f(1.0, 1.0, -1.0);
        #
        # glTexCoord2f(0.0, 0.0);
        # glVertex3f(1.0, -1.0, -1.0);
        #
        # glTexCoord2f(0.0, 1.0);
        # glVertex3f(-1.0, 1.0, -1.0);
        # glTexCoord2f(0.0, 0.0);
        # glVertex3f(-1.0, 1.0, 1.0);
        # glTexCoord2f(1.0, 0.0);
        # glVertex3f(1.0, 1.0, 1.0);
        # glTexCoord2f(1.0, 1.0);
        # glVertex3f(1.0, 1.0, -1.0);
        # glTexCoord2f(1.0, 1.0);
        # glVertex3f(-1.0, -1.0, -1.0);
        # glTexCoord2f(0.0, 1.0);
        # glVertex3f(1.0, -1.0, -1.0);
        # glTexCoord2f(0.0, 0.0);
        # glVertex3f(1.0, -1.0, 1.0);
        # glTexCoord2f(1.0, 0.0);
        # glVertex3f(-1.0, -1.0, 1.0);
        # glTexCoord2f(1.0, 0.0);
        # glVertex3f(1.0, -1.0, -1.0);
        # glTexCoord2f(1.0, 1.0);
        # glVertex3f(1.0, 1.0, -1.0);
        # glTexCoord2f(0.0, 1.0);
        # glVertex3f(1.0, 1.0, 1.0);
        # glTexCoord2f(0.0, 0.0);
        # glVertex3f(1.0, -1.0, 1.0);
        # glTexCoord2f(0.0, 0.0);
        # glVertex3f(-1.0, -1.0, -1.0);
        # glTexCoord2f(1.0, 0.0);
        # glVertex3f(-1.0, -1.0, 1.0);
        # glTexCoord2f(1.0, 1.0);
        # glVertex3f(-1.0, 1.0, 1.0);
        # glTexCoord2f(0.0, 1.0);
        # glVertex3f(-1.0, 1.0, -1.0);
        # glEnd()

    def _DrawTerrain_with_VAO(self):

        if not len(self._game_scene.chunks):
            print("Error Chunk array is empty! ")
        for chunk in self._game_scene.chunks:
            glBindVertexArray(chunk.VAO)
            glDrawElements(GL_TRIANGLE_STRIP, len(chunk.index_array), GL_UNSIGNED_INT, None)
            # glDrawArrays(GL_TRIANGLE_STRIP, 0, 6)

    def display(self):
        delta_time = time.time()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glLoadIdentity()
        self._make_camera(self._camera_obj.get_postion(), self._camera_obj.get_point_of_view())
        glScalef(1.0, 2.0, 1.0)

        if 0:
            glLineWidth(1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if 1:
            self._DrawTerrain_with_VAO()
        else:
            self.set_shaders(self.default_vertexShaderSource, self.default_fragmentShaderSource)
            self._draw_terrain(0)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor3f(1.0, 0.0, 1.0)
        glutSolidCube(0.05)
        glFlush()
        delta_time = time.time() - delta_time  # The more the worse
        #print("Delta time: ", delta_time)

    def opengl_error_check(self):
        error = glGetError()
        if error != GL_NO_ERROR:
            print("OPENGL_ERROR: ", gluErrorString(error))

    def INfutureForDestrustor(self):
        # Опционально: освобождаем        все        ресурсы, как        только
        #  они        выполнили        свое        предназначение
        # glDeleteVertexArrays(1, & VAO);
        # glDeleteBuffers(1, & VBO);
        # glDeleteBuffers(1, & EBO);
        pass

    def Keyboard(self, key, x, y):
        cam_angel = self._camera_obj.cam_angel
        cam_angel_h = self._camera_obj.cam_angel_h
        rotate_angle = self._camera_obj.CAMERA_ANGEL

        if key == GLUT_KEY_UP:  # Клавиша вверх
            self._camera_obj.move_forward(cam_angel)
        elif key == GLUT_KEY_DOWN:  # Клавиша вниз
            self._camera_obj.move_back(cam_angel)
        elif key == GLUT_KEY_LEFT:  # Клавиша влево
            cam_angel -= rotate_angle
        elif key == GLUT_KEY_RIGHT:  # Клавиша вправо
            cam_angel += rotate_angle
        elif key == GLUT_KEY_PAGE_UP:  # Клавиша вниз
            cam_angel_h += rotate_angle
        elif key == GLUT_KEY_HOME:  # Клавиша вниз Y
            self._camera_obj.move_up()
        elif key == GLUT_KEY_END:
            self._camera_obj.move_down()
        elif key == GLUT_KEY_PAGE_DOWN:  # Клавиша вниз
            cam_angel_h -= rotate_angle  # math.cos(cam_angel * math.pi / 180) * CAMERA_SPEED
        self._camera_obj.rotate(cam_angel, cam_angel_h)
        # glutPostRedisplay()
