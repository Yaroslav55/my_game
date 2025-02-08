import numpy as np

from scene import Vector3f




class BaseEntity:
    name: str = None
    position: Vector3f = Vector3f(0, 0, 0)
    directionOfMovement: Vector3f = Vector3f(0, 0, 0)
    velocityOfMovement: Vector3f = Vector3f(0.1, 0.1, 0.1)

    def __init__(self, name: str):
        self.name = name

class Model(BaseEntity):
    info: list[str] = list()
    # Vertices[x, y, z], Color[r, g, b], Texture coord[x, y]
    model_data: np.array = None

    vertex_indices: list[int] = list()
    texture_name: str = "tiles/Basic_Buch_Tiles_Compiled.png"

    def __init__(self, name: str, mesh_info, data_arr, indices):
        super().__init__(name)
        self.mesh_info = mesh_info
        self.model_data = data_arr
        self.vertex_indices = indices

class Entity(Model):
    pass
