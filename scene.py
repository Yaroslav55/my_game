
import const_variables_store as const_var
from backend.debug_logger import Logger

from backend.entities.entities import Mesh, Vector3f, Entity, Model


class Scene(object):
    def __init__(self, ):

        self.lines_aray = [Vector3f(0, 0, 0) for i in range(300)]
        self.models: list[Mesh] = list()


    def add_entity(self, entity: Entity):
        if isinstance(entity, Model):
            self.models.append( entity )
        else:
            Logger.warn(f"Unsupported entity format: {entity}")

    def draw_grid(self, grid_size=1) -> None:
        grid_size = const_var.GRID_UNIT
        num_lines = 40
        max_len = num_lines * grid_size
        start_old_line = Vector3f(max_len / (-2), 0, -max_len / 2)
        for i in range(num_lines * 4 + 1)[::4]:
            if i == 0:
                self._render.lines_aray[i].set(start_old_line)
                self._render.lines_aray[i + 1].set_variables(start_old_line.x,
                                                             start_old_line.y,
                                                             start_old_line.z + max_len)

                self._render.lines_aray[i + 2].set(start_old_line)
                self._render.lines_aray[i + 3].set_variables(start_old_line.x + max_len,
                                                             start_old_line.y,
                                                             start_old_line.z)
            else:
                start_old_line.set(self._render.lines_aray[i - 4])
                start_old_line.x += grid_size
                self._render.lines_aray[i].set(start_old_line)
                self._render.lines_aray[i + 1].set_variables(start_old_line.x,
                                                             start_old_line.y,
                                                             start_old_line.z + max_len)
                start_old_line.set(self._render.lines_aray[i - 2])
                start_old_line.z += grid_size
                self._render.lines_aray[i + 2].set(start_old_line)
                self._render.lines_aray[i + 3].set_variables(start_old_line.x + max_len,
                                                             start_old_line.y,
                                                             start_old_line.z)

        print("d")

    def _set_txt_coord(self, posX, posY):
        tile_w = 512
        tile_h = 122
        txt_size = 16
        unit_X = 1 / (tile_w / txt_size)
        unit_Y = 1 / (tile_h / txt_size)
        txtr_posU = unit_X * posX
        txtr_posV = unit_Y * posY

        return txtr_posU, txtr_posV
