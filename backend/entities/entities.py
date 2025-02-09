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

    def __add__(self, value):
        if isinstance(value, __class__):
            return self.__class__(self.x + value.x, self.y + value.y, self.z + value.z)
        else:  # Increase on constant
            return self.__class__(self.x + value, self.y + value, self.z + value)


class BaseEntity:
    name: str = None
    position: Vector3f = Vector3f(0, 0, 0)
    directionOfMovement: Vector3f = Vector3f(0, 0, 0)
    velocityOfMovement: Vector3f = Vector3f(0.1, 0.1, 0.1)
    def __init__(self, name: str):
        self.name = name

class Mesh:
    mesh_info: list[str] = list()
    # Vertices[x, y, z], Color[r, g, b], Texture coord[x, y]
    model_data: np.array = None
    vertex_indices: np.array = np.empty(0, dtype=np.int32)
    texture_name: str = "models/wood.png"

    def __init__(self, mesh_info: list[str], data_arr: np.array, indices: list[int]):
        self.mesh_info = mesh_info
        self.model_data = data_arr
        self.vertex_indices = indices
        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.material = None

class Model(BaseEntity, Mesh):

    def __init__(self, name: str, mesh_info, data_arr, indices):
        super().__init__(name)
        self.mesh_info = mesh_info
        self.model_data = data_arr
        self.vertex_indices = indices

class Entity(Model):
    pass
