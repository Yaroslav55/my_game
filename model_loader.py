from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageFile

from backend.debug_logger import Logger
from backend.entities.entities import Model
from backend.tiles.common import set_singleton
from scene import Vector3f


class ObjLoader():

    @dataclass
    class MainSymbols:
        COMMENT: str = '#'
        VERTEX: str = 'v'
        TEXT_COORDS: str = 'vt'
        VERTEX_NORM: str = 'vn'
        FRAGMENT: str = 'f'

    # @staticmethod
    # def _manage_shared_vertex(  mesh_data: np.array, vertex_indx, texture_coord : list) -> [np.array, int]:
    #     fragment_index = vertex_indx
    #     if not all(mesh_data[vertex_indx][6: ]):
    #         mesh_data[vertex_indx][3: ] = [1, 1, 1, *texture_coord]
    #     elif any(mesh_data[vertex_indx][6: ] != texture_coord):
    #         tmp_vertex_data = [*mesh_data[vertex_indx][0:3], 0, 0, 1, *texture_coord ]
    #         mesh_data = np.append(mesh_data, [tmp_vertex_data], axis=0 )
    #         fragment_index = len(mesh_data) -1
    #     return mesh_data, fragment_index

    @staticmethod
    def _manage_shared_vertex(  mesh_data, vertex_indx, texture_coord) -> int:
        fragment_index = vertex_indx
        if not mesh_data[vertex_indx][6: ]:
            mesh_data[vertex_indx].extend([*[1, 1, 1], *texture_coord])
        elif mesh_data[vertex_indx][6: ] != texture_coord:
            mesh_data.append( [*mesh_data[vertex_indx][0:3], *[0, 0, 1], *texture_coord ] )
            fragment_index = len(mesh_data) -1
        return fragment_index

    def get_count_of_elements(self, model_data):
        start_data = {
            self.MainSymbols.TEXT_COORDS: None,
            self.MainSymbols.VERTEX_NORM: None,
            self.MainSymbols.VERTEX: None,
            self.MainSymbols.FRAGMENT: None,
        }
        element_count = {
            self.MainSymbols.TEXT_COORDS: None,
            self.MainSymbols.VERTEX_NORM: None,
            self.MainSymbols.VERTEX: None,
            self.MainSymbols.FRAGMENT: None,
        }
        last_symb = [self.MainSymbols.VERTEX, 0]
        for line_num, line in enumerate(model_data):
            for data_type, start in start_data.items():
                if data_type in line:
                    if start_data[data_type] is None:
                        start_data[data_type] = line_num
                        element_count[last_symb[0]] = last_symb[1]
                    last_symb = [data_type, line_num]
                    break
        else:
            element_count[last_symb[0]] = last_symb[1]

        for k, v in element_count.items():
            element_count[k] = v - start_data[k] +1
        return start_data, element_count


    # @classmethod
    def load_model(self, model_name, model_pos: Vector3f = Vector3f(0, 18, 0), scale: float = 1) -> Model:
        with open(model_name, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line != '\n']

        start_data, element_count = self.get_count_of_elements(model_data=lines)

        mesh_data = list()
        fragments: np.array = np.empty(element_count[self.MainSymbols.FRAGMENT] * 3, dtype=np.int32)
        info_data: list[str] = list()
        f_index = 0
        for index, line in enumerate(lines):
            split_line = line.split()
            if self.MainSymbols.COMMENT is split_line[0]:
                info_data.append(line)
            elif self.MainSymbols.FRAGMENT is split_line[0]:
                for vect_indxs in split_line[1:]:
                    vertex_indx, text_indx, normal_indx = [ int(indxs) -1 for indxs in vect_indxs.split('/')]
                    texture_coord_line = lines[ start_data[self.MainSymbols.TEXT_COORDS] + text_indx ].split()
                    texture_coord = texture_coord_line[1: ]

                    vertex_indx = self._manage_shared_vertex(mesh_data, vertex_indx, texture_coord)
                    # fragments = np.append(fragments, vertex_indx)
                    fragments[f_index] = vertex_indx
                    f_index += 1
            elif self.MainSymbols.VERTEX is split_line[0]:
                vector_real_pos = Vector3f( *[float(x) for x in split_line[1:]] )
                vector_real_pos *= scale
                vector_real_pos += model_pos
                mesh_data.append([*vector_real_pos])
            # else:
            #     Logger.warn(f"In loading model {model_name}, line: {split_line}")

        # fragments = fragments.astype(np.int32)
        model_mesh = Model(name=model_name, mesh_info=info_data,
                           data_arr=np.array(mesh_data, dtype='f'), indices=fragments)
        return model_mesh

class ImageLoader:

    # images: dict[str: ImageFile.ImageFile] = dict()
    test_img_name: str = 'test_tail.png'
    test_img_full: str = 'backend/tiles/test_tail.png'

    @classmethod
    def load_image(cls, path_to_file: Path) -> ImageFile.ImageFile:
        img = Image.open(path_to_file)
        cls.process_tiles(cls, img)
        return Image.open(path_to_file)

    def show(self, path_to_file: Path) -> None:
        img = Image.open(path_to_file)
        img.show()

    def process_tiles(self, image_source: ImageFile.ImageFile) -> ImageFile.ImageFile:

        # image_source = image_source.resize(image_source.size, resample=Image.Resampling.BILINEAR)
        # image_source.show()
        return image_source.quantize(colors=3).convert('RGB')

        # image_source = image_source.resize(image_source.size, resample=Image.Resampling.LANCZOS  )
        # image_source = image_source.filter(filter=ImageFilter.UnsharpMask(radius=100, percent=100, threshold=3))

@set_singleton
class Loader:

    supported_model_formats = {'.obj': ObjLoader()}
    image_loader = ImageLoader()

    @staticmethod
    def check_file_exists(method):
        def wrapper(*args, **kwargs):
            path = Path(kwargs['path_to_file'])
            if path.is_file():
                kwargs['path_to_file'] = path
                return method(*args, **kwargs)
            Logger.err(f"File {path.name} not found in {path.parent}")
            return None

        return wrapper

    @check_file_exists
    def load_model(self, path_to_file: str| Path, model_pos: Vector3f = Vector3f(0, 18, 0),
                   scale: float = 0.5) -> Model:

        if path_to_file.suffix in self.supported_model_formats.keys():
            loader_obj = self.supported_model_formats[path_to_file.suffix]
            return  loader_obj.load_model(path_to_file, model_pos, scale)
        Logger.warn(f"Unsupported format: {path_to_file}")


    @check_file_exists
    def load_image(self, path_to_file: Path):
        return self.image_loader.load_image(path_to_file=path_to_file)
