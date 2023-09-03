# Yaroslav 2023

from scene import Scene
from camera import Camera
from render import Render

GAME_MODE = "3D"
RENDER_API = "Opengl"

global renderer
global game_scene


def update():
    pass
    # renderer.update_frame( update )


def game_init():
    game_scene.draw_terrain(16)
    # game_scene.draw_terrain(4)
    # game_scene.draw_terrain(4)
    # game_scene.draw_grid(0.5)


if __name__ == "__main__":

    game_camera = Camera(0.0, 3.0, 4.0, -90, 90)  # Class of main game camera
    game_scene = Scene()
    if RENDER_API == "Opengl":
        renderer = Render(game_camera, game_scene, update)

    game_init()

    renderer.run()  # Start game loop
