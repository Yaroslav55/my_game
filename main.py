# Yaroslav 2023
from __future__ import annotations

from backend.graphic_engine.graphic_manager import GraphicManager
from camera import Camera2D, Camera3D
from const_variables_store import GAME_MODE
from scene import Scene, Vector3f


from model_loader import Loader


def update():
    pass
    # renderer.update_frame( update )


def game_init():
    pass



def run_game():
    if GAME_MODE == "2D":
        game_camera = Camera2D(33.0, 120.0, 77.0, 0, -190)  # Class of main game camera
    else:
        game_camera = Camera3D(10.0, 10.0, 14.0, -90, -90)  # Class of main game camera

    model = Loader()
    game_scene = Scene()
    # new = model.load_model("models/tinker.obj", model_pos =Vector3f(0, 0, 0), scale=1)
    cube = model.load_model("models/textured_cube.obj", model_pos =Vector3f(0, 4, -5), scale=10)
    # game_scene.add_entity( cube )
    game_camera.set_player_mesh(cube)
    game_init()

    render = GraphicManager(game_camera, game_scene, update)
    render.run()  # Start game loop

if __name__ == "__main__":
    run_game()
