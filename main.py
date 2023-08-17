# Yaroslav 2023
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time
import math

from scene import Scene
from camera import Camera
from render import Render

GAME_MODE = "3D"
RENDER_API = "Opengl"
CAMERA_SPEED = 4
CAMERA_ANGEL = 5
delta_time = 0
GAME_TIMER = 15  # ms


cam_angel = -90
cam_angel_h = 90  # Angel for 3D scene
# renderer = Render()
# game_scene = Scene()
#game_camera = Camera(0.0, 0.0, 17.0, cam_angel, cam_angel_h)  # Class of main game camera

h = 5
w = 5


global renderer
global game_scene
def update():

    print("eee")
    #renderer.update_frame( update )



# def _draw_terrain(line_mode: bool = 0):
#     #       Draw game terrain
#     if line_mode:
#         glLineWidth(1)
#         glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
#     else:
#         glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
#
#     glBegin(GL_TRIANGLE_STRIP)
#     glColor3d(0, 1, 0)
#     for i in game_scene.index_array:
#         try:
#             x = game_scene.vertex_array[i - 1][0]
#             y = game_scene.vertex_array[i - 1][1]
#             z = game_scene.vertex_array[i - 1][2]
#             glVertex3d(x, y, z)
#         except IndexError:
#             print("Error: Triangle index dont have a vertex pair: index ", i - 1)
#     glEnd();
#     #       -------------


# def display():
#     global delta_time
#     delta_time = time.time()
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#
#     glLoadIdentity()
#     _pos = game_camera.get_postion()
#     _look = game_camera.get_point_of_view()
#     if GAME_MODE == "3D":
#         gluLookAt(_pos[0], _pos[1], _pos[2], _look[0], _look[1], _look[2], 0.0, 1.0, 0.0)
#     elif GAME_MODE == "2D":
#         pass
#     glScalef(1.0, 2.0, 1.0);
#
#     game_scene.draw_grid()
#     _draw_terrain(1)
#     # glColor3f(1.0, 1.0, 1.0)
#     # glutWireCube(1.0)
#     glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
#     glColor3f(1.0, 0.0, 1.0)
#     glutSolidCube(0.05)
#
#     glFlush()
#     delta_time = time.time() - delta_time




# def reshape(w, h):
#     glViewport(0, 0, w, h);
#     glMatrixMode(GL_PROJECTION);
#     glLoadIdentity();
#     glFrustum(-0.5, 0.5, -1.0, 1.0, 1.5, 40.0);
#     glMatrixMode(GL_MODELVIEW);
#

if __name__ == "__main__":

    game_camera = Camera(0.0, 0.0, 17.0, cam_angel, cam_angel_h)  # Class of main game camera

    if RENDER_API == "Opengl":
        renderer = Render(game_camera, update)
        game_scene = Scene(renderer)

    game_scene.draw_terrain(5, 5)

    renderer.run()             # Start game loop

    # glutInit(sys.argv)
    # glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    # glutInitWindowSize(800, 800)
    # glutInitWindowPosition(100, 100)
    # glutCreateWindow("Transformed Cube")
    # init()
    # glutDisplayFunc(display)
    # glutSpecialFunc(Keyboard)
    # glutReshapeFunc(reshape)
    # glutTimerFunc(GAME_TIMER, update, 0)
    # glutMainLoop()
