from enum import Enum

from PIL import ImageFile

from backend.debug_logger import Logger
from backend.entities.entities import Vector3f
from scene import Scene


class MapGenerator:

    TILE_SIZE = 512 * 0.25
    TILE_MAX: Vector3f = Vector3f(TILE_SIZE, TILE_SIZE)
    TILE_V: Vector3f = Vector3f().get_vector(TILE_MAX, TILE_MAX * (-1))
    class MapElements(Enum):
        EMPTY_SPACE: int = 49
        ROADS: int = 18
        BUILDS: int = 38


    def texture_coord_to_global_coord(self, x, y, z= 0):

        global_point: Vector3f =  Vector3f(x, y, z) - self.TILE_V / 2
        return global_point * 0.5

    @classmethod
    def foo(cls, img: ImageFile.ImageFile):

        img_pixels = img.load()
        width, height = img.size
        i = 0
        for y in range(height):
            for x in range(width):
                if img_pixels[x, y] == (0, 0, 0, 255):
                    world_pos: Vector3f = cls.texture_coord_to_global_coord(cls, x, y)
                    world_pos = Vector3f(world_pos.x, 4, world_pos.y)
                    i += 1
                    Logger.err(f"x {x}, w_z {y}")
                    Logger.err(f"w_x {world_pos.x}, w_z {world_pos.z}\n")
                    # Logger.err(Scene().)
                    Scene().add_cube(position=world_pos, size=0.25)
        print(f"i {i}")
