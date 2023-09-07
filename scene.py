import math

import const_variables_store as const_var
from typing import List
import numpy as np


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

    def set(self, coord: List[List[int]]):
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
        else:  # Increase on constant
            return self.__class__(self.x + value, self.y + value, self.z + value)

class Mesh(object):
    MAX_VERTEX_COUNT = 81
    def __init__(self):
        # One vertex = [ positionXYZ, ColorRGB, TexCoord ] - 8 variables * type float 4 byte - 32 bytes
        self.vertex_array = np.empty((self.MAX_VERTEX_COUNT, 8), dtype='f')
        self.index_array = []
        self.texture = "test_img.jpg"
        self.VAO = None
        self.VBO = None
        self.EBO = None

    def __del__(self):
        pass
class GameChunk(Mesh):
    #MAX_VERTEX_COUNT = 81 // const_var.TERRAIN_UNIT

    def __init__(self, pos: Vector3f, size):
        Mesh.__init__(self)
        self.chunk_position: Vector3f = Vector3f(pos.x, pos.y, pos.z)
        self.chunk_size = size
        self.numb_of_faces = size // const_var.TERRAIN_UNIT + 1
        self.numb_of_triangles = 0
        # self.vertex_array = [ [0] * 3 for i in range(self.MAX_VERTEX_COUNT)]
        # self.vertex_array = np.empty((self.MAX_VERTEX_COUNT, 3), dtype='f')
        # self.index_array = []

        # self.vertexBuffer_ID = None
        # self.indexBuffer_ID = None

    def __del__(self):
        pass


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
        chunk = GameChunk(offset_vector, size)

        # chunk.vertex_array[0][0] = 0
        # chunk.vertex_array[0][1] = 0
        # chunk.vertex_array[0][2] = 0
        # # Color
        # chunk.vertex_array[0][3] = 1.0
        # chunk.vertex_array[0][4] = 0.0
        # chunk.vertex_array[0][5] = 1.0
        # # Texture coord
        # chunk.vertex_array[0][6] = 0.0
        # chunk.vertex_array[0][7] = 0.0
        # #################
        # chunk.vertex_array[1][0] = 5
        # chunk.vertex_array[1][1] = 0
        # chunk.vertex_array[1][2] = 0
        # # Color
        # chunk.vertex_array[1][3] = 1.0
        # chunk.vertex_array[1][4] = 0.0
        # chunk.vertex_array[1][5] = 1.0
        # # Texture coord
        # chunk.vertex_array[1][6] = 1.0
        # chunk.vertex_array[1][7] = 0.0
        # ##################
        # chunk.vertex_array[2][0] = 5
        # chunk.vertex_array[2][1] = 5
        # chunk.vertex_array[2][2] = 0
        # # Color
        # chunk.vertex_array[2][3] = 1.0
        # chunk.vertex_array[2][4] = 0.0
        # chunk.vertex_array[2][5] = 1.0
        # # Texture coord
        # chunk.vertex_array[2][6] = 1.0
        # chunk.vertex_array[2][7] = 1.0

        chunk_len = chunk.numb_of_faces # Chunk length in faces
        row = 0
        count_of_indx_for_chunk = chunk_len * chunk_len - (chunk_len - 1)
        upper_texture_index = [(0.0, 1.0), (1.0, 1.0)]
        lower_texture_index = [(0.0, 0.0), (1.0, 0.0)]

        txt_index = 0
        for i in range(chunk_len):
            for j in range(chunk_len):
                # Position
                chunk.vertex_array[j + row][0] = (terrain_unit * j) + offset_vector.x
                chunk.vertex_array[j + row][1] = terrain_unit * i + offset_vector.y
                chunk.vertex_array[j + row][2] = 0 + offset_vector.z
                # Color
                chunk.vertex_array[j + row][3] = 1.0
                chunk.vertex_array[j + row][4] = 0.0
                chunk.vertex_array[j + row][5] = 1.0
                # Texture coord
                if i % 2 == 0:
                    curent_text_coord = lower_texture_index[txt_index]
                else:
                    curent_text_coord = upper_texture_index[txt_index]
                txt_index += 1
                if txt_index >= 2:
                    txt_index = 0
                print(curent_text_coord)
                chunk.vertex_array[j + row][6] = curent_text_coord[0]
                chunk.vertex_array[j + row][7] = curent_text_coord[1]
                # chunk.vertex_array[j + row] += offset_vector
            txt_index = 0
            row += chunk_len

        for i in range(count_of_indx_for_chunk)[1::]:
            if i == 1:
                chunk.index_array.append(0)
            if i % chunk_len == 0:
                #       Always will be one extra degenerate triangle
                chunk.index_array.append(i + size)
                chunk.index_array.append(i + size)
                chunk.index_array.append(i)
                chunk.index_array.append(i)
            else:
                chunk.index_array.append(i + size)
                chunk.index_array.append(i)
        chunk.numb_of_triangles = len(chunk.index_array)
        self.chunks.append(chunk)  # Adding chunk to draw

    def draw_terrain(self, size):
        offset_vector: Vector3f = Vector3f()
        self._make_terrain(size, offset_vector)
        DIST_X = 2
        DIST_Y = 2
        # for i in range(DIST_Y):
        #     for j in range(DIST_X):
        #         self._make_terrain(size, offset_vector)
        #         offset_vector.x = self.chunks[-1].chunk_size + self.chunks[-1].chunk_position.x
        #         # print( "i and j: ", i, j )
        #     offset_vector.y = self.chunks[-1].chunk_size + self.chunks[-1].chunk_position.y
        #     offset_vector.x = self.chunks[0].chunk_position.x
        print("-Info: Terrain was created!")
