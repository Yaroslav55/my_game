from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

import time
import numpy as np
from typing import Union

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
        self.VBO = None

    def run(self):
        self._opengl_init()

    def _opengl_init(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(100, 100)
        glutCreateWindow("Transformed Cube")
        # Old init func

        # # Create the VBO
        # vertices = np.array([[0, 1, 0], [-1, -1, 0], [1, -1, 0]], dtype='f')
        # self.vertexPositions = vbo.VBO(vertices)
        #
        # # Create the index buffer object
        # self.indices = np.array([[0, 1, 2]], dtype=np.int32)
        # self.indexPositions = vbo.VBO(self.indices, target=GL_ELEMENT_ARRAY_BUFFER)

        glClearColor(0.5, 0.5, 0.5, 1.0)
        glShadeModel(GL_FLAT)
        # -------
        glutDisplayFunc(self.display)
        glutSpecialFunc(self.Keyboard)
        glutReshapeFunc(self.reshape)
        glutTimerFunc(self._GAME_TIMER, self.update_frame, 0)
        glutMainLoop()

    def update_frame(self, value):
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
        if line_mode:
            glLineWidth(1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        for index, chunk in enumerate(self._game_scene.chunks):
            # if index == 0:
            start_index = 0
            # else:
            #     start_index = self._game_scene.chunks[ index -1].area * 2 -1
            last_index = int(start_index + (chunk.numb_of_faces * chunk.numb_of_faces) * 2 - 1)
            glBegin(GL_TRIANGLE_STRIP)
            glColor3d(1, 1, 0)
            for i in chunk.index_array[start_index:last_index]:
                try:
                    x = chunk.vertex_array[i - 1].x
                    y = chunk.vertex_array[i - 1].y
                    z = chunk.vertex_array[i - 1].z
                    glVertex3d(x, y, z)
                except IndexError:
                    print("Error: Triangle index dont have a vertex pair: index ", i - 1)
            glEnd()
        #       -------------

    def reshape(self, w, h):
        glViewport(0, 0, w, h);
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glFrustum(-0.5, 0.5, -1.0, 1.0, 1.5, 40.0);
        glMatrixMode(GL_MODELVIEW);

    def _make_camera(self, pos: Union[Vector3f, list[float]], look: Union[Vector3f, list[float]]):

        if self.GAME_MODE == "3D":
            gluLookAt(pos[0], pos[1], pos[2], look[0], look[1], look[2], 0.0, 1.0, 0.0)
        elif self.GAME_MODE == "2D":
            pass

    def VBO_enable(self):

        # Create the VBO
        # #vertices = np.array([[0, 1, 0], [-1, -1, 0], [1, -1, 0]], dtype='f')
        # vertex_array = [[0] * 3 for i in range(25)]
        # indx_array = self._game_scene.chunks[0].index_array
        # if len(self._game_scene.chunks):
        #     for i in range(25):
        #         vertex_array[i][0] = self._game_scene.chunks[0].vertex_array[i].x
        #         vertex_array[i][1] = self._game_scene.chunks[0].vertex_array[i].y
        #         vertex_array[i][2] = self._game_scene.chunks[0].vertex_array[i].z
        #     # for i in range(161):
        #     #     indx_array[i] = self._game_scene.chunks[0].index_array[i].x
        #     #

        #index_buffer = (1, 6, 2, 7, 3, 8, 4, 9, 5, 10, 10, 6, 6, 11, 7, 12, 8, 13, 9, 14, 10, 15)
        index_buffer = (1, 6)#, 2, 7, 3, 8, 4, 9, 5, 10, 6, 11, 7, 12, 8, 13, 9, 14, 10, 15)
        vertex_arr: list[list[float]] = [
            [3, 5, 0], [4, 5, 0], [5, 5, 0], [6, 5, 0], [7, 5, 0],
            [3, 4, 0], [4, 4, 0], [5, 4, 0], [6, 4, 0], [7, 4, 0],
            [3, 3, 0], [4, 3, 0], [5, 3, 0], [6, 3, 0], [7, 3, 0]
        ]


        vertices = np.array(vertex_arr, dtype='f')
        self.vertexPositions = vbo.VBO(vertices)

        # Create the index buffer object
        self.indices = np.array(index_buffer, dtype=np.int32)
        self.indexPositions = vbo.VBO(self.indices, target=GL_ELEMENT_ARRAY_BUFFER)


        self.indexPositions.bind()
        glColor3f(1.0, 0.0, 1.0)
        glLineWidth(1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        self.vertexPositions.bind()
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        # glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
        glDrawElements(GL_TRIANGLE_STRIP, 30, GL_UNSIGNED_INT, None)  # This line does work too!

    def display(self):
        global delta_time
        delta_time = time.time()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        self._make_camera(self._camera_obj.get_postion(), self._camera_obj.get_point_of_view())
        glScalef(1.0, 2.0, 1.0)

        # self._draw_lines()

        # self._draw_terrain(const_var.TERRAIN_MODE)
        self.VBO_enable()
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        # glColor3f(1.0, 0.0, 1.0)
        # glutSolidCube(0.05)

        glFlush()
        delta_time = time.time() - delta_time

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
