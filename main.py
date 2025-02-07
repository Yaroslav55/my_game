# Yaroslav 2023
from __future__ import annotations

from scene import Scene
from camera import *
from openglrender import OpenGLRender
from model_loader import Loader

GAME_MODE = "2D"
RENDER_API = "Opengl"


def update():
    pass
    # renderer.update_frame( update )


def game_init():
    pass


def dec_init(func):
    def wrapper():
        if GAME_MODE == "2D":
            game_camera = Camera2D(33.0, 120.0, 77.0, 0, -190)  # Class of main game camera
        else:
            game_camera = Camera3D(10.0, 10.0, 14.0, -90, -90)  # Class of main game camera
        if RENDER_API == "Opengl":
            render_cls = OpenGLRender
        func(render_cls, game_camera)
    return wrapper

@dec_init
def run_game(renger_cls: OpenGLRender, came_obj: Camera2D | Camera3D):
    model = Loader()
    game_scene = Scene()
    game_scene.draw_terrain(3)
    came_obj.set_player_mesh(model.load_model("models/tinker.obj", scale=10))
    game_init()

    render = renger_cls(came_obj, game_scene, update)
    render.run()  # Start game loop

if __name__ == "__main__":
    run_game()
