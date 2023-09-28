import math
import random
import time

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

    def is_empty(self):
        if (self.x == 0) and (self.y == 0) and (self.z == 0):
            return True
        else:
            return False

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

    # Overload "==" operator
    def __eq__(self, arg_2) -> bool:
        if isinstance(arg_2, self.__class__):
            if self.x == arg_2.x:
                if self.y == arg_2.y:
                    if self.z == arg_2.z:
                        return True
        return False

    def __add__(self, value):
        if isinstance(value, __class__):
            return self.__class__(self.x + value.x, self.y + value.y, self.z + value.z)
        else:  # Increase on constant
            return self.__class__(self.x + value, self.y + value, self.z + value)


class Mesh(object):
    MAX_VERTEX_COUNT = 2378

    def __init__(self):
        self.info = {"type": "model", "model_name": ""}
        # One vertex = [ positionXYZ, ColorRGB, TexCoordUV ] - 8 variables * type float 4 byte - 32 bytes
        self.vertex_array = np.empty((self.MAX_VERTEX_COUNT, 8), dtype='f')
        self.index_array = []
        self.mesh_position: Vector3f = Vector3f(0, 0, 0)
        self.directionOfMovement: Vector3f = Vector3f(0, 0, 0)
        self.velocityOfMovement: Vector3f = Vector3f(0.1, 0.1, 0.1)
        self.texture_name = "tiles/Basic_Buch_Tiles_Compiled.png"
        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.material = None

    def __del__(self):
        pass


class GameChunk(Mesh):
    # MAX_VERTEX_COUNT = 81 // const_var.TERRAIN_UNIT

    def __init__(self, pos: Vector3f, size):
        Mesh.__init__(self)
        self.mesh_position = Vector3f(pos.x, pos.y, pos.z)
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
    def __init__(self, ):

        self.lines_aray = [Vector3f(0, 0, 0) for i in range(300)]
        self.chunks: GameChunk = []
        self.models: list[Mesh] = []

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
        tile_h = 224
        txt_size = 16
        unit_X = 1 / (tile_w / txt_size)
        unit_Y = 1 / (tile_h / txt_size)
        txtr_posU = unit_X * posX
        txtr_posV = unit_Y * posY
        return txtr_posU, txtr_posV

    def _make_terrain(self, size, offset_vector: Vector3f):
        # index_buffer = (1, 6, 2, 7, 3, 8, 4, 9, 5, 10, 10, 6, 6, 11, 7, 12, 8, 13, 9, 14, 10, 15)
        # vertex_arr: list[list[float]] = [
        #     [3, 5, 0], [4, 5, 0], [5, 5, 0], [6, 5, 0], [7, 5, 0],
        #     [3, 4, 0], [4, 4, 0], [5, 4, 0], [6, 4, 0], [7, 4, 0],
        #     [3, 3, 0], [4, 3, 0], [5, 3, 0], [6, 3, 0], [7, 3, 0]
        # ]
        terrain_unit = const_var.TERRAIN_UNIT
        chunk = GameChunk(offset_vector, size)

        chunk_len = chunk.numb_of_faces  # Chunk length in faces
        row = 0
        const_w = 32
        const_h = 14
        count_of_indx_for_chunk = chunk_len * chunk_len - (chunk_len - 1)
        lower_texture_index = ((0.0 / const_w, 1.0 / const_h), (1.0 / const_w, 1.0 / const_h))
        upper_texture_index = ((0.0 / const_w, 0.0 / const_h), (1.0 / const_w, 0.0 / const_h))
        txt_index = 0

        def create_vertex(_i, _j, cur_txtr: tuple, UV_pos: tuple):
            _tmp_array: List[float] = [0] * 8
            # Position
            _tmp_array[0] = (terrain_unit * _j) + offset_vector.x
            _tmp_array[1] = 0 + offset_vector.y
            _tmp_array[2] = terrain_unit * _i + offset_vector.z
            # Color
            _tmp_array[3] = 1.0
            _tmp_array[4] = 0.0
            _tmp_array[5] = 1.0
            # Texture coord
            txtr_pos = self._set_txt_coord(cur_txtr[0], cur_txtr[1])
            _tmp_array[6] = UV_pos[0] + txtr_pos[0]
            _tmp_array[7] = UV_pos[1] + txtr_pos[1]
            # chunk.vertex_array[j + row] += offset_vector
            return _tmp_array

        _tmp_vertex_aray = list()
        for i in range(chunk_len):
            for j in range(chunk_len):
                # curr_txtr = (12, 5)
                curr_txtr = (random.randrange(12, 15), 5)
                _tmp_vertex_aray.append(create_vertex(i, j, curr_txtr, upper_texture_index[0]))
                _tmp_vertex_aray.append(create_vertex(i, j - 1, curr_txtr, lower_texture_index[0]))
                _tmp_vertex_aray.append(create_vertex(i + 1, j, curr_txtr, upper_texture_index[1]))
                _tmp_vertex_aray.append(create_vertex(i + 1, j - 1, curr_txtr, lower_texture_index[1]))
            row += chunk_len
        for i in range(len(_tmp_vertex_aray))[0::4]:
            chunk.index_array.append(i)
            chunk.index_array.append(i + 1)
            chunk.index_array.append(i + 2)

            chunk.index_array.append(i + 1)
            chunk.index_array.append(i + 2)
            chunk.index_array.append(i + 3)
            # if i == 1:
            #     chunk.index_array.append(0)
            # if i % (chunk_len * 2)  == 0:
            #     #       Always will be one extra degenerate triangle
            #     chunk.index_array.append(i )
            #     chunk.index_array.append(i -1)
            #     chunk.index_array.append(i)
            #     # chunk.index_array.append(i)
            # else:
            # chunk.index_array.append(i)
            #     chunk.index_array.append(i + size)
            #     chunk.index_array.append(i)
        chunk.numb_of_triangles = len(chunk.index_array)
        chunk.vertex_array = np.array(_tmp_vertex_aray, dtype='f')
        self.chunks.append(chunk)  # Adding chunk to draw

    def generate_vegetation(self, amount):
        from model_loader import Loader
        loader = Loader()
        for i in range(amount):
            poss = Vector3f(random.randrange(0, 150), 10, random.randrange(0, 150))
            model = loader.load_model("models/model.obj", poss, 0.01)
            self.models.append(model)

    def draw_terrain(self, size):
        delta_time = time.time()
        offset_vector: Vector3f = Vector3f(0, 0, 0)
        # self._make_terrain(size, offset_vector)
        DIST_X = 25
        DIST_Y = 25
        for i in range(DIST_Y):
            for j in range(DIST_X):
                self._make_terrain(size, offset_vector)
                offset_vector.x = self.chunks[-1].chunk_size + self.chunks[-1].mesh_position.x
                # print( "i and j: ", i, j )
            offset_vector.z = self.chunks[-1].chunk_size + self.chunks[-1].mesh_position.z
            offset_vector.x = self.chunks[0].mesh_position.x
        print("-Info: Terrain was created!")
        print("Time spent for creating terrain ", time.time() - delta_time)
