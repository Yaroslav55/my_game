import math

import const_variables_store as const_var


class Vector3f:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def set_variables(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def set_zero(self):
        self.set_variables(0.0, 0.0, 0.0)

    def set(self, coord: list[list[int]]):
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]

    def set(self, coord: None):
        self.x = coord.x
        self.y = coord.y
        self.z = coord.z

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            print("Error Vector3F incorrect index: ", index)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            print("Error Vector3F incorrect index: ", index)

    def __add__(self, value):
        if isinstance(value, __class__):
            return self.__class__(self.x + value.x, self.y + value.y, self.z + value.z)
        else:       # Increase on constant
            return self.__class__(self.x + value, self.y + value, self.z + value)


class GameChunk(object):
    MAX_VERTEX_COUNT = 289 // const_var.TERRAIN_UNIT

    def __init__(self, pos: Vector3f, size):
        self.chunk_position: Vector3f = Vector3f(pos.x, pos.y, pos.z )
        self.chunk_size = size
        self.numb_of_faces = size // const_var.TERRAIN_UNIT + 1

        self.vertex_array = [Vector3f(0, 0, 0) for i in range(self.MAX_VERTEX_COUNT)]
        self.index_array = []


class Scene(object):
    def __init__(self):

        self.lines_aray = [Vector3f(0, 0, 0) for i in range(300)]
        self.chunks: GameChunk = []

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

    def _make_terrain(self, size, offset_vector: Vector3f):
        # index_buffer = (1, 6, 2, 7, 3, 8, 4, 9, 5, 10, 10, 6, 6, 11, 7, 12, 8, 13, 9, 14, 10, 15)
        # vertex_arr: list[list[float]] = [
        #     [3, 5, 0], [4, 5, 0], [5, 5, 0], [6, 5, 0], [7, 5, 0],
        #     [3, 4, 0], [4, 4, 0], [5, 4, 0], [6, 4, 0], [7, 4, 0],
        #     [3, 3, 0], [4, 3, 0], [5, 3, 0], [6, 3, 0], [7, 3, 0]
        # ]
        terrain_unit = const_var.TERRAIN_UNIT
        #offset_vector.z = 0
        chunk = GameChunk(offset_vector, size)
        chunk_len = chunk.numb_of_faces  # Chunk length in faces
        row = 0
        count_of_indx_for_chunk = chunk_len * chunk_len - (chunk_len - 1)
        for i in range(chunk_len):
            for j in range(chunk_len):
                chunk.vertex_array[j + row].set_variables(terrain_unit * j, terrain_unit * i, 0)
                chunk.vertex_array[j + row] += offset_vector
            row += chunk_len
        for i in range(count_of_indx_for_chunk)[1::]:
            if i == 1:
                chunk.index_array.append(1)
            if i % chunk_len == 0:
                #       Always will be one extra degenerate triangle
                chunk.index_array.append(i + chunk_len)
                chunk.index_array.append(i + chunk_len)
                chunk.index_array.append(i + 1)
                chunk.index_array.append(i + 1)
            else:
                chunk.index_array.append(i + chunk_len)
                chunk.index_array.append(i + 1)

        self.chunks.append(chunk)  # Adding chunk to draw

    def draw_terrain(self, size):
        offset_vector: Vector3f = Vector3f()
        DIST = 10
        for i in range(DIST):
            for j in range(DIST):
                self._make_terrain(size, offset_vector)  # + One addition border
                offset_vector.x = self.chunks[-1].chunk_size + self.chunks[-1].chunk_position.x
                print( "i and j: ", i, j )
            offset_vector.y = self.chunks[-1].chunk_size + self.chunks[-1].chunk_position.y
            offset_vector.x = self.chunks[0].chunk_position.x
        print("-Info: Terrain was created!")
