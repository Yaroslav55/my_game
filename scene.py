import math

from render import Render, Vector3f
import const_variables_store as const_var

class Scene(object):

    def __init__(self, render_Obj: Render):
        self._render = render_Obj


    def draw_grid(self, grid_size = 1) -> None:
        grid_size = const_var.GRID_UNIT
        num_lines = 40
        max_len = num_lines * grid_size
        start_old_line = Vector3f(max_len / (-2), 0, -max_len/2)
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
                start_old_line.set( self._render.lines_aray[i - 4] )
                start_old_line.x += grid_size
                self._render.lines_aray[i].set( start_old_line )
                self._render.lines_aray[i + 1].set_variables(start_old_line.x,
                                                             start_old_line.y,
                                                             start_old_line.z + max_len)
                start_old_line.set( self._render.lines_aray[i - 2] )
                start_old_line.z += grid_size
                self._render.lines_aray[i + 2].set(start_old_line)
                self._render.lines_aray[i + 3].set_variables(start_old_line.x + max_len,
                                                             start_old_line.y,
                                                             start_old_line.z)

        print("d")

    def _make_terrain(self, hight, width):
        # index_buffer = (1, 6, 2, 7, 3, 8, 4, 9, 5, 10, 10, 6, 6, 11, 7, 12, 8, 13, 9, 14, 10, 15)
        # vertex_arr: list[list[float]] = [
        #     [3, 5, 0], [4, 5, 0], [5, 5, 0], [6, 5, 0], [7, 5, 0],
        #     [3, 4, 0], [4, 4, 0], [5, 4, 0], [6, 4, 0], [7, 4, 0],
        #     [3, 3, 0], [4, 3, 0], [5, 3, 0], [6, 3, 0], [7, 3, 0]
        # ]
        offset_vector = Vector3f( -hight / 2, 0, -width / 2)
        row = 0
        for i in range(hight):
            for j in range(width):
                self._render.vertex_array[j + row][0] = j
                self._render.vertex_array[j + row][1] = 0
                self._render.vertex_array[j + row][2] = i
                self._render.vertex_array[j + row] += offset_vector
            row += hight
        for i in range(hight * width - (hight - 1))[1::]:
            if i == 1:
                self._render.index_array.append(1)
            if i % hight == 0:
                #       Always will be one extra degenerate triangle
                self._render.index_array.append(i + width)
                self._render.index_array.append(i + width)
                self._render.index_array.append(i + 1)
                self._render.index_array.append(i + 1)
            else:
                self._render.index_array.append(i + width)
                self._render.index_array.append(i + 1)


    def draw_terrain(self, hight, width):
        self._make_terrain(hight, width)
        print("-Info: Terrain was created!")
