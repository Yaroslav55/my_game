from dataclasses import dataclass

import numpy as np

from backend.debug_logger import Logger
from backend.entities.entities import Model
from scene import Vector3f, Mesh


class Loader(object):

    @dataclass
    class MainSymbols:
        COMMENT: str = '#'
        VERTEX: str = 'v'
        TEXT_COORDS: str = 'vt'
        VERTEX_NORM: str = 'vn'
        FRAGMENT: str = 'f'


    def load_model(self, model_name, model_pos: Vector3f = Vector3f(0, 18, 0), scale = 0.5):

        #scale = 0.01
        obj_center_vec = model_pos
        #position = Vector3f(0, 0, 0)
        try:
            with open(model_name, 'r') as file:
                lines = file.readlines()        # Read all data
                file.close()
                model_mesh = Mesh()
                model_mesh.mesh_position = obj_center_vec
                model_mesh.directionOfMovement.set_variables( obj_center_vec.x, obj_center_vec.y, obj_center_vec.z)
                model_mesh.info["model_name"] = model_name
                txtr__coord_array = []
                iter_v = 0
                for line in lines:
                    if line[0] == '\n':
                        continue
                    line = line.replace('\t', '')
                    line = line.replace('\n', '')
                    line = line.split(' ')
                    if line[0] == 'v':
                        # Vector of length
                        obj_vec = Vector3f( (obj_center_vec.x - float(line[1])) * scale,
                                            (obj_center_vec.y + float(line[2])) * scale,
                                            (obj_center_vec.z - float(line[3])) * scale)
                        model_mesh.vertex_array[iter_v][0] = obj_center_vec.x + obj_vec.x     # X
                        model_mesh.vertex_array[iter_v][1] = obj_center_vec.y + obj_vec.y     # Y
                        model_mesh.vertex_array[iter_v][2] = obj_center_vec.z + obj_vec.z     # Z
                        iter_v += 1
                    elif line[0] == 'vt':
                        line.pop(0)
                        txtr__coord_array.append(line)
                    elif line[0] == 'f':
                        for element in line[1::]:
                            element = element.split('/')
                            element = list(map(int, element))           # Conver str list to int list
                            model_mesh.index_array.append(int(element[0]) - 1)
                            if txtr__coord_array:       # If txtr coord exist in model file
                                model_mesh.vertex_array[element[0] - 1][6] = txtr__coord_array[element[1] - 1][0]
                                model_mesh.vertex_array[element[0] - 1][7] = txtr__coord_array[element[1] - 1][1]
                    elif line[0] == 'vn':
                        pass
                    elif line[1] == "#end":
                        print( "Model ", model_name, "was loaded" )
                    else:
                        print("Unknown start symbol ", line[0], "in", model_name)
                model_mesh.texture_name = "models/LeavesTransparent.png"
                return model_mesh
        except IOError:
            print("Error: could not open model " + model_name)
            return -2
        print("Something go wrong ", model_name)
        return -3


    def load_mode_nl(self, model_name, model_pos: Vector3f = Vector3f(0, 18, 0), scale = 0.5) -> Model:
        with open(model_name, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line != '\n' ]

        start_data = {
            self.MainSymbols.VERTEX: int,
            # self.MainSymbols.TEXT_COORDS: int,
            self.MainSymbols.VERTEX_NORM: int,
        }
        for data_type, start in start_data.items():
            for line_num, line in enumerate(lines):
                if  self.MainSymbols.COMMENT in line:
                    continue
                if data_type in line:
                    start_data[data_type] = line_num
                    break

        mesh_data = list()
        fragments: list[int] = list()
        info_data: list[str] = list()
        for index, line in enumerate(lines):
            split_line = line.split()
            if self.MainSymbols.COMMENT in split_line[0]:
                info_data.append(line)
            elif self.MainSymbols.FRAGMENT in split_line[0]:
                fragments.extend( [ int(inx[0])-1 for inx in split_line[1:]])
            elif self.MainSymbols.VERTEX in split_line[0]:
                related_text_coor: list[str] = [1, 1, 1]
                related_normal: list[str] = [1, 1]
                x, y, z = [float(x) for x in split_line[1:]]
                vector_real_pos = Vector3f(x, y, z)
                vector_real_pos += model_pos
                vector_real_pos *= scale

                mesh_data.append( [*vector_real_pos, *related_normal, *related_text_coor]  )
            else:
                Logger.warn(f"In loading model {model_name}, line: {split_line}")

        model_mesh = Model(name=model_name, mesh_info= info_data,
                           data_arr=np.array(mesh_data, dtype='f'), indices=fragments)
        return model_mesh


    def load_model_new(self, model_name: str, model_pos: Vector3f = Vector3f(0, 18, 0), scale = 1) -> Model:
        """from Figuro at https://www.figuro.io"""
        with open(model_name, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        start_data = {
            self.MainSymbols.VERTEX: int,
            self.MainSymbols.TEXT_COORDS: int,
            self.MainSymbols.VERTEX_NORM: int,
        }
        for data_type, start in start_data.items():
            for line_num, line in enumerate(lines):
                if data_type in line:
                    start_data[data_type] = line_num
                    break

        tmp_ar = list()
        fragments: list[int] = list()
        info_data: list[str] = list()
        for index, line in enumerate(lines):
            if not line:
                continue

            split_line = line.split()
            if self.MainSymbols.COMMENT in split_line[0]:
                info_data.append(line)
            elif self.MainSymbols.FRAGMENT in split_line[0]:
                fragments.extend( [ int(inx[0]) for inx in split_line[1:]])
            elif self.MainSymbols.VERTEX_NORM in split_line[0]:
                related_text_coor: list[str] = lines[start_data[self.MainSymbols.TEXT_COORDS]].split()[1:]
                related_normal: list[str] = lines[start_data[self.MainSymbols.VERTEX_NORM]].split()[1:]
                tmp_ar.extend( [*split_line[1:], *related_normal, *related_text_coor,]  )

                start_data =  { k: d+1 for k, d in start_data.items() }
            else:
                print(f"{split_line}")

        return Model(info_data, tmp_ar, fragments)
