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

    def set(self, coord: list[list[int]]):
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]

    def get_vector(self, vec_1,
                           vec_2):
        vec_1 = np.array( [vec_1] )
        vec_2 = np.array( [vec_2])
        d = (vec_1 - vec_2)[0]
        return Vector3f( *d )

    def get_distance(self, vec_1: list,
                           vec_2: list) -> float:

        return np.linalg.norm(self.get_vector(*vec_1, *vec_2))

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
        return self.x

    def __iter__(self):
        return iter( [self.x, self.y, self.z] )

    def __len__(self):
        return 1

    def __imul__(self, value: float):
        """In-place multiplication: multiply each element of the list by 'other'."""
        self.x *= value
        self.y *= value
        self.z *= value
        return self

    # Overload "==" operator
    def __eq__(self, arg_2) -> bool:
        if isinstance(arg_2, self.__class__):
            if self.x == arg_2.x:
                if self.y == arg_2.y:
                    if self.z == arg_2.z:
                        return True
        return False

    def __mul__(self, value: float):
            return Vector3f(self.x * value, self.y * value, self.z * value)

    def __truediv__(self, value: float):
        return Vector3f(self.x / value, self.y / value, self.z / value)

    def __add__(self, value):
        if isinstance(value, self.__class__):
            return self.__class__(self.x + value.x, self.y + value.y, self.z + value.z)
        else:  # Increase on constant
            return self.__class__(self.x + value, self.y + value, self.z + value)

    def __sub__(self, value):
        if isinstance(value, self.__class__):
            return self.__class__(self.x - value.x, self.y - value.y, self.z - value.z)
        else:  # Increase on constant
            return self.__class__(self.x - value, self.y - value, self.z - value)

class BaseEntity:
    # name: str = None
    position: Vector3f = Vector3f(0, 0, 0)
    directionOfMovement: Vector3f = Vector3f(0, 0, 0)
    velocityOfMovement: Vector3f = Vector3f(0.1, 0.1, 0.1)

    def __init__(self, **kwargs):
        self.name = None
        for field, value in kwargs.items():
            setattr(self, field, value)
        print("f")
class Mesh(BaseEntity):

    mesh_info: list[str] = [0,]
    # Vertices[x, y, z], Color[r, g, b], Texture coord[x, y]
    model_data: np.array = None
    vertex_indices: np.array = np.empty(0, dtype=np.int32)
    texture_name: str = "models/wood.png"

    def __init__(self, mesh_info: list[str], data_arr: np.array, indices: list[int], **kwargs ):
        super().__init__(**kwargs)
        self.mesh_info.extend( mesh_info )
        self.model_data = data_arr
        self.vertex_indices = indices
        self.need_update_mesh: bool = True

        #----------------------------------
        self.model_centre = np.mean(self.model_data[: 3], axis=0)
        self.model_min = np.min(self.model_data[: 3], axis=0)
        self.model_max = np.max(self.model_data[: 3], axis=0)
        self.diagonal = Vector3f().get_vector(self.model_max, self.model_min)

        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.material = None

    def update_geometry(self):
        for vertex in self.model_data:
            vertex_pos: Vector3f = Vector3f(*vertex[0: 3])
            vertex_pos += self.position
            vertex[0: 3] = vertex_pos

    def clear_model_data(self):
        """
        If model is static and also was uploaad in video memory(VBO, VAO)
        we can delete not necessary vertex date
        :return: None
        """
        if not self.need_update_mesh:
            del self.model_data
            del self.vertex_indices

    def make_copy(self, position: Vector3f):
        new_object: Mesh = Mesh(mesh_info=[], data_arr=self.model_data.copy(),
                                indices=self.vertex_indices.copy(), position=position
                                )
        new_object.need_update_mesh = True
        new_object.texture_name = 'test_img.jpg'
        new_object.mesh_info[0] += 1
        new_object.update_geometry()
        return new_object


class Model(Mesh):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Entity(Model):
    pass
