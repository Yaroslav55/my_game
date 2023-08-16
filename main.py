# Yaroslav 2023
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time
import math

from camera import Camera
from scene import Scene

GAME_MODE = "3D"
CAMERA_SPEED = 4
CAMERA_ANGEL = 5
delta_time = 0
GAME_TIMER = 15  # ms
game_scene = Scene()

cam_angel = -90
cam_angel_h = 90  # Angel for 3D scene

game_camera = Camera(0.0, 0.0, 17.0, cam_angel, cam_angel_h)  # Class of main game camera


def update(value):
    # print(delta_time )
    glutPostRedisplay()
    glutTimerFunc(GAME_TIMER, update, 0)


def init():
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glShadeModel(GL_FLAT)


def test():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glutWireCube(1.0)
    glutPostRedisplay()


def display():
    global delta_time
    delta_time = time.time()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    _pos = game_camera.get_postion()
    _look = game_camera.get_point_of_view()
    if GAME_MODE == "3D":
        gluLookAt(_pos[0], _pos[1], _pos[2], _look[0], _look[1], _look[2], 0.0, 1.0, 0.0)
    elif GAME_MODE == "2D":
        pass
    glScalef(1.0, 2.0, 1.0);

    game_scene.draw_grid()

    # glColor3f(1.0, 1.0, 1.0)
    # glutWireCube(1.0)
    index_buffer = (1, 6, 2, 7, 3, 8, 4, 9, 5, 10, 10, 6, 6, 11, 7, 12, 8, 13, 9, 14, 10, 15)
    vertex_arr: list[list[float]] = [
        [3, 5, 0], [4, 5, 0], [5, 5, 0], [6, 5, 0], [7, 5, 0],
        [3, 4, 0], [4, 4, 0], [5, 4, 0], [6, 4, 0], [7, 4, 0],
        [3, 3, 0], [4, 3, 0], [5, 3, 0], [6, 3, 0], [7, 3, 0]
    ]
    glLineWidth(1)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_TRIANGLE_STRIP)
    glColor3d(0, 1, 0)
    h = 5
    w = 5
    vert_arr = [ [0] *3 for i in range( h * w) ]
    index_arr = []
    offset = 1
    row = 0
    for i in range(h):
        for j in range(w):
            vert_arr[j + row][0] = 3 + j
            vert_arr[j + row][1] = 5 - i
            vert_arr[j + row][2] = 0
        row += h
    index_arr.append(1)
    for i in range(9)[1::]:
        index_arr.append(i + w )
        index_arr.append(i + 1)
    for i in index_buffer:
        x = vert_arr[i - 1][0]
        y = vert_arr[i - 1][1]
        z = vert_arr[i - 1][2]
        #print("index: ", i, "vertex: ", vertex_arr[i - 1])
        glVertex3d(x, y, z)
    glEnd();
    # glPolygonMode(GL_FRONT_AND_BACK , GL_FILL)
    # glPushMatrix()
    # glColor3f(1.0, 0.0, 1.0)
    # glTranslate(3, 0, 5)
    # glutSolidCube(1.0)
    # glPopMatrix()

    glFlush()
    delta_time = time.time() - delta_time


def Keyboard(key, x, y):
    global cam_angel, cam_angel_h

    if key == GLUT_KEY_UP:  # Клавиша вверх
        game_camera.move_forward(cam_angel, CAMERA_SPEED)
    elif key == GLUT_KEY_DOWN:  # Клавиша вниз
        game_camera.move_back(cam_angel, CAMERA_SPEED)
    elif key == GLUT_KEY_LEFT:  # Клавиша влево
        cam_angel -= CAMERA_ANGEL
    elif key == GLUT_KEY_RIGHT:  # Клавиша вправо
        cam_angel += CAMERA_ANGEL  # Увеличиваем угол вращения по оси Y
    elif key == GLUT_KEY_PAGE_UP:  # Клавиша вниз
        cam_angel_h += CAMERA_ANGEL
    elif key == GLUT_KEY_HOME:  # Клавиша вниз Y
        game_camera.move_up(CAMERA_ANGEL)
    elif key == GLUT_KEY_END:
        game_camera.move_down(CAMERA_ANGEL)
    elif key == GLUT_KEY_PAGE_DOWN:  # Клавиша вниз
        cam_angel_h -= CAMERA_ANGEL  # math.cos(cam_angel * math.pi / 180) * CAMERA_SPEED
    game_camera.rotate(cam_angel, cam_angel_h)
    # glutPostRedisplay()


def reshape(w, h):
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glFrustum(-0.5, 0.5, -1.0, 1.0, 1.5, 40.0);
    glMatrixMode(GL_MODELVIEW);


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Transformed Cube")
    init()
    glutDisplayFunc(display)
    glutSpecialFunc(Keyboard)
    glutReshapeFunc(reshape)
    glutTimerFunc(GAME_TIMER, update, 0)
    glutMainLoop()
