
from backend.debug_logger import Logger

from backend.entities.entities import Mesh, Vector3f, Model
from backend.tiles.common import set_singleton
from model_loader import Loader

@set_singleton
class Scene(object):
    def __init__(self, ):

        self.lines_aray = [Vector3f(0, 0, 0) for i in range(300)]
        self.models: list[Mesh] = list()
        self.cube_model: Model = Loader().load_model(path_to_file="models/textured_cube.obj", model_pos=Vector3f(0, 0, 0), scale=0.25)

    def add_entity(self, entity: Mesh):
        if isinstance(entity, Mesh):
            self.models.append( entity )
        else:
            Logger.warn(f"Unsupported entity format: {entity}")

    def add_cube(self, position: Vector3f, size: float):
        new_cube = self.cube_model.make_copy(position=position)
        self.add_entity( entity=new_cube )
