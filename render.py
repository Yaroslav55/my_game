from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
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

        self.vertexShaderSource = """
                    #version 330 core
                    layout (location = 0) in vec3 aPos;
                    layout (location = 1) in vec3 aColor;
                    out vec3 ourColor;
                        void main()
                        {
                            gl_Position = vec4(aPos, 1.0);
                            ourColor = aColor;
                    }"""
        self.fragmentShaderSource = """
                    #version 330 core
                    out vec4 FragColor;
                    in vec3 ourColor;
                        void main()
                        {
                            FragColor = vec4(ourColor, 1.0f);
                        }
                    """
        self.VAO = None
        self.VBO = None
        self.vertices = np.array((
            # positions       colors
         0.5, -0.5, 0.0,   1.0, 0.0, 0.0,       # bottom right
        -0.5, -0.5, 0.0,   0.0, 1.0, 0.0,       # bottom left
         0.0,  0.5, 0.0,   0.0, 0.0, 1.0        # top
        ), dtype='f')
    def run(self):
        self._opengl_init()

    def VBO_init(self):
        # Create the VBO
        if not len(self._game_scene.chunks):
            return -1
        for chunk in self._game_scene.chunks:
            chunk.vertexBuffer_ID = vbo.VBO(chunk.vertex_array, usage=GL_STATIC_DRAW)
            # Create the index buffer object
            indices = np.array(chunk.index_array, dtype=np.int32)
            chunk.indexBuffer_ID = vbo.VBO(indices, usage=GL_STATIC_DRAW, target=GL_ELEMENT_ARRAY_BUFFER)
            chunk.indexBuffer_ID.bind()
            glEnableVertexAttribArray(0)

    # Процедура подготовки шейдера (тип шейдера, текст шейдера)
    def shader_init(self):
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, self.vertexShaderSource)
        glCompileShader(vertexShader)
        success = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)
        if not success:
            info_mesg = glGetShaderInfoLog(vertexShader)
            print("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n", info_mesg)
        # fragment        shader
        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, self.fragmentShaderSource)
        glCompileShader(fragmentShader)
        # check for shader compile errors
        success = glGetShaderiv(fragmentShader, GL_COMPILE_STATUS)
        if not success:
            info_mesg = glGetShaderInfoLog(fragmentShader)
            print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n", info_mesg)
        # link        shaders

        shaderProgram = glCreateProgram()
        glAttachShader(shaderProgram, vertexShader)
        glAttachShader(shaderProgram, fragmentShader)
        glLinkProgram(shaderProgram)
        # check        for linking errors
        success = glGetProgramiv(shaderProgram, GL_LINK_STATUS)
        if not success:
            info_mesg = glGetProgramInfoLog(shaderProgram)
            print( "ERROR::SHADER::PROGRAM::LINKING_FAILED\n", info_mesg )
        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        # bind        the        Vertex        Array        Object        first, then        bind and set        vertex        buffer(s), and then        configure        vertex        attributes(s).
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * 4, self.vertices, GL_STATIC_DRAW)

        # position        attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 6 * 4, None)
        glEnableVertexAttribArray(0)
        # color        attribute
        glVertexAttribPointer(1, 3, GL_FLOAT, False, 6 * 4, c_void_p(12))
        glEnableVertexAttribArray(1)
        glUseProgram(shaderProgram)


    def _opengl_init(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(100, 100)
        glutCreateWindow("Transformed Cube")
        # Old init func
        # self.VBO_init()
        self.shader_init()
        print(float(glGetString(GL_VERSION)[:3]))

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

        #       Draw game terrain
        for index, chunk in enumerate(self._game_scene.chunks):
            start_index = 0
            last_index = int(start_index + (chunk.numb_of_faces * chunk.numb_of_faces) * 2 - 1)
            glBegin(GL_TRIANGLE_STRIP)
            glColor3d(1, 1, 0)
            for i in chunk.index_array[start_index:last_index]:
                try:
                    x = chunk.vertex_array[i][0]
                    y = chunk.vertex_array[i][1]
                    z = chunk.vertex_array[i][2]
                    glVertex3d(x, y, z)
                except IndexError:
                    print("Error: Triangle index dont have a vertex pair: index ", i - 1)
            glEnd()
        #       -------------

    def reshape(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-0.5, 0.5, -1.0, 1.0, 1.5, 40.0)
        glMatrixMode(GL_MODELVIEW);

    def _make_camera(self, pos: Union[Vector3f, List[float]], look: Union[Vector3f, List[float]]):

        if self.GAME_MODE == "3D":
            gluLookAt(pos[0], pos[1], pos[2], look[0], look[1], look[2], 0.0, 1.0, 0.0)
        elif self.GAME_MODE == "2D":
            pass

    def drawCube(self):
        glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        def load_textureToGPU():
            im = None
            try:
                im = Image.open("test_img.jpg")
                convert = im.convert("RGBA")
                image_data = convert.tobytes()
            except OSError:
                print("Cannot open img")
                return -1
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 288, 288,
                         0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
            glGenerateMipmap(GL_TEXTURE_2D)

            return texture

        glBindTexture(GL_TEXTURE_2D, load_textureToGPU())
        glVertexPointer(3, GL_FLOAT, 0, None)
        """Draw a cube with texture coordinates"""
        glBegin(GL_QUADS);
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-1.0, -1.0, 1.0);
        glTexCoord2f(1.0, 0.0);
        glVertex3f(1.0, -1.0, 1.0);
        glTexCoord2f(1.0, 1.0);
        glVertex3f(1.0, 1.0, 1.0);
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-1.0, 1.0, 1.0);
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-1.0, -1.0, -1.0);
        glTexCoord2f(1.0, 1.0);
        glVertex3f(-1.0, 1.0, -1.0);
        glTexCoord2f(0.0, 1.0);
        glVertex3f(1.0, 1.0, -1.0);
        glTexCoord2f(0.0, 0.0);
        glVertex3f(1.0, -1.0, -1.0);
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-1.0, 1.0, -1.0);
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-1.0, 1.0, 1.0);
        glTexCoord2f(1.0, 0.0);
        glVertex3f(1.0, 1.0, 1.0);
        glTexCoord2f(1.0, 1.0);
        glVertex3f(1.0, 1.0, -1.0);
        glTexCoord2f(1.0, 1.0);
        glVertex3f(-1.0, -1.0, -1.0);
        glTexCoord2f(0.0, 1.0);
        glVertex3f(1.0, -1.0, -1.0);
        glTexCoord2f(0.0, 0.0);
        glVertex3f(1.0, -1.0, 1.0);
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-1.0, -1.0, 1.0);
        glTexCoord2f(1.0, 0.0);
        glVertex3f(1.0, -1.0, -1.0);
        glTexCoord2f(1.0, 1.0);
        glVertex3f(1.0, 1.0, -1.0);
        glTexCoord2f(0.0, 1.0);
        glVertex3f(1.0, 1.0, 1.0);
        glTexCoord2f(0.0, 0.0);
        glVertex3f(1.0, -1.0, 1.0);
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-1.0, -1.0, -1.0);
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-1.0, -1.0, 1.0);
        glTexCoord2f(1.0, 1.0);
        glVertex3f(-1.0, 1.0, 1.0);
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-1.0, 1.0, -1.0);
        glEnd()

    def _DrawTerrain_with_VBO(self):

        # Create the VBO
        if not len(self._game_scene.chunks):
            print("Error Chunk array is empty! ")
            return -1
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 0.0, 1.0)

        for chunk in self._game_scene.chunks:
            chunk.vertexBuffer_ID.bind()
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            # glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
            glDrawElements(GL_TRIANGLE_STRIP, chunk.numb_of_triangles, GL_UNSIGNED_INT,
                           None)  # This line does work too!

    def VAO_enable(self):
        pass

    def display(self):
        global delta_time
        delta_time = time.time()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glLoadIdentity()
        self._make_camera(self._camera_obj.get_postion(), self._camera_obj.get_point_of_view())
        glScalef(1.0, 2.0, 1.0)

        if 1:
            glLineWidth(1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # self.VAO_enable()
        #self.drawCube()
        # self._draw_lines()
        # glDeleteVertexArrays(1, [self.VAO])
        # glDeleteBuffers(1, [self.VBO])
        # glDeleteProgram(shaderProgram)
        self._draw_terrain(const_var.TERRAIN_MODE)
        # self._DrawTerrain_with_VBO()

        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        # glColor3f(1.0, 0.0, 1.0)
        # glutSolidCube(0.05)
        print("eee ")
        glutSwapBuffers()
        #glFlush()
        delta_time = time.time() - delta_time  # The more the worse
        # print("Delta time: ", delta_time)

    def opengl_error_check(self):
        error = glGetError()
        if error != GL_NO_ERROR:
            print("OPENGL_ERROR: ", gluErrorString(error))

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
