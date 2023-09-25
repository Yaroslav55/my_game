# Yaroslav 2023

from scene import Scene
from camera import *
from render import Render
from model_loader import Loader

GAME_MODE = "3D"
RENDER_API = "Opengl"

global renderer
global game_scene


def update():
    pass
    # renderer.update_frame( update )


def game_init():
    pass
    #game_scene.draw_terrain(8)
    # game_scene.draw_terrain(4)
    # game_scene.draw_terrain(4)
    # game_scene.draw_grid(0.5)


if __name__ == "__main__":

    # game_camera = Camera(10.0, 10.0, 14.0, -90, -190)  # Class of main game camera
    model = Loader()
    game_scene = Scene()
    if GAME_MODE == "2D":
        game_camera = Camera2D(16.0, 12.0, 77.0, 0, -190)  # Class of main game camera
    else:
        game_camera = Camera3D(10.0, 10.0, 14.0, -90, -90)  # Class of main game camera

    game_camera.set_player_mesh(model.load_model("models/model.obj"))
    if RENDER_API == "Opengl":
        renderer = Render(game_camera, game_scene, update)

    game_init()
    renderer.run()  # Start game loop
