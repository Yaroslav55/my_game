# Yaroslav 2023
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

from camera import Camera

GAME_MODE = "3D"
CAMERA_SPEED = 4
CAMERA_ANGEL = 5

class Coordinate:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


starter_cam_pos = Coordinate(0.0, 0.0, 5.0)
global cam_angel
global cam_angel_h
game_camera = Camera( starter_cam_pos.x, starter_cam_pos.y, starter_cam_pos.z )  # Class of main game camera


def init():
    global cam_angel, cam_angel_h
    cam_angel = 0
    # cam_angel_h = 90 Angel for 3D scene
    cam_angel_h = 180

    glClearColor(0.5, 0.5, 0.5, 1.0)
    glShadeModel(GL_FLAT)


def display():
    global cam_angel, cam_angel_h
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()
    _pos = game_camera.get_postion()
    _look = game_camera.get_point_of_view()
    gluLookAt(_pos[0], _pos[1], _pos[2], _look[0], _look[1], _look[2], 0.0, 1.0, 0.0)
    glScalef(1.0, 2.0, 1.0);

    glColor3f(0, 1, 1);
    i = -30
    while i < 30:
        glBegin(GL_LINES);
        glVertex3f(-10, -1, i);
        glVertex3f(10, -1, i);
        glEnd();

        glBegin(GL_LINES);
        glVertex3f(i, -1, -10);
        glVertex3f(i, -1, 10);
        glEnd();
        i += 1
    glColor3f(1.0, 1.0, 1.0)
    glutWireCube(1.0)

    glPushMatrix()
    glColor3f(1.0, 0.0, 1.0)
    glTranslate(3, 0, 5)
    glutSolidCube(1.0)
    glPopMatrix()
    #
    # glBegin(GL_LINES);
    # glVertex3f(-2, 0, 0);
    # glVertex3f(2, 0, 0);
    # glEnd();
    # glBegin(GL_LINES);
    # glVertex3f(0, -2, 0);
    # glVertex3f(0, 2, 0);
    # glEnd();
    glFlush();


def Keyboard(key, x, y):
    global cam_angel, cam_angel_h
    if cam_angel == 360 or cam_angel == -360:
        cam_angel = 0

    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:  # Клавиша вверх
        game_camera.move_forward(cam_angel, CAMERA_SPEED)
    elif key == GLUT_KEY_DOWN:  # Клавиша вниз
        game_camera.move_back(cam_angel, CAMERA_SPEED)
    elif key == GLUT_KEY_LEFT:  # Клавиша влево
        cam_angel -= CAMERA_ANGEL
    elif key == GLUT_KEY_RIGHT:  # Клавиша вправо
        cam_angel += CAMERA_ANGEL  # Увеличиваем угол вращения по оси Y
    elif key == GLUT_KEY_PAGE_UP:  # Клавиша вниз
        cam_angel_h += math.cos(cam_angel * math.pi / 180) * CAMERA_SPEED
    elif key == GLUT_KEY_PAGE_DOWN:  # Клавиша вниз
        cam_angel_h -= math.cos(cam_angel * math.pi / 180) * CAMERA_SPEED
    #print(cam_angel)
    game_camera.rotate(cam_angel)
    glutPostRedisplay()  # Вызываем процедуру перерисовки


def reshape(w, h):
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glFrustum(-0.5, 0.5, -1.0, 1.0, 1.5, 20.0);
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
    glutMainLoop()
