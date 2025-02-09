from dataclasses import dataclass

import numpy as np

from backend.debug_logger import Logger
from backend.entities.entities import Model
from scene import Vector3f


class ObjLoader():

    @dataclass
    class MainSymbols:
        COMMENT: str = '#'
        VERTEX: str = 'v'
        TEXT_COORDS: str = 'vt'
        VERTEX_NORM: str = 'vn'
        FRAGMENT: str = 'f'

    @staticmethod
    def _manage_shared_vertex(  mesh_data, vertex_indx, texture_coord) -> int:
        fragment_index = vertex_indx
        if not mesh_data[vertex_indx][6: ]:
            mesh_data[vertex_indx].extend([*[1, 1, 1], *texture_coord])
        elif mesh_data[vertex_indx][6: ] != texture_coord:
            mesh_data.append( [*mesh_data[vertex_indx][0:3], *[0, 0, 1], *texture_coord ] )
            fragment_index = len(mesh_data) -1
        return fragment_index

    @classmethod
    def load_model(cls, model_name, model_pos: Vector3f = Vector3f(0, 18, 0), scale=0.5) -> Model:
        with open(model_name, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line != '\n']

        start_data = {
            cls.MainSymbols.VERTEX: int,
            cls.MainSymbols.TEXT_COORDS: int,
            cls.MainSymbols.VERTEX_NORM: int,
        }
        for data_type, start in start_data.items():
            for line_num, line in enumerate(lines):
                if cls.MainSymbols.COMMENT in line:
                    continue
                if data_type in line:
                    start_data[data_type] = line_num
                    break

        mesh_data = list()
        fragments: np.array = np.empty(0, dtype=np.int32)
        info_data: list[str] = list()
        for index, line in enumerate(lines):
            split_line = line.split()
            if cls.MainSymbols.COMMENT is split_line[0]:
                info_data.append(line)
            elif cls.MainSymbols.FRAGMENT is split_line[0]:
                for vect_indxs in split_line[1:]:
                    vertex_indx, text_indx, normal_indx = [ int(indxs) -1 for indxs in vect_indxs.split('/')]
                    texture_coord_line = lines[ start_data[cls.MainSymbols.TEXT_COORDS] + text_indx ].split()
                    texture_coord = texture_coord_line[1: ]

                    vertex_indx = cls._manage_shared_vertex(mesh_data, vertex_indx, texture_coord)
                    fragments = np.append(fragments, vertex_indx)

            elif cls.MainSymbols.VERTEX is split_line[0]:
                vector_real_pos = Vector3f( *[float(x) for x in split_line[1:]] )
                vector_real_pos += model_pos
                vector_real_pos *= scale
                mesh_data.append([*vector_real_pos])
            else:
                Logger.warn(f"In loading model {model_name}, line: {split_line}")

        fragments = fragments.astype(np.int32)
        model_mesh = Model(name=model_name, mesh_info=info_data,
                           data_arr=np.array(mesh_data, dtype='f'), indices=fragments)
        return model_mesh

class Loader:

    supported_model_formats = {'.obj': ObjLoader}
    def load_model(self, model_name, model_pos: Vector3f = Vector3f(0, 18, 0), scale = 0.5) -> Model | int:

        for format, loader in self.supported_model_formats.items():
            if format in model_name:
                loader_obj = self.supported_model_formats[format]
                return  loader_obj.load_model(model_name, model_pos, scale)
        Logger.warn(f"Cant load entity {model_name}")
        return -1
