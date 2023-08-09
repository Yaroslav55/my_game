import math


class Vector3f:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class Camera(object):
    GAME_MODE = "3D"

    def __init__(self, pos_x, pos_y, pos_z, angle=0, angle_top=90):
        self._cam_angel = 0.0
        self._cam_angel_h = 90  # Angel for 3D scene
        # self.cam_angel_h = 180
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._pos_z = pos_z

    def move_forward(self, angle, speed = 0):
        self._pos_x += math.cos(self._cam_angel * math.pi / 180) * speed
        self._pos_z += math.sin(self._cam_angel * math.pi / 180) * speed
        # self._cam_pos.z += math.sin(self._cam_angel * math.pi / 180) * speed

    def move_back(self, angle, speed=0):
        self._pos_x -= math.cos(self._cam_angel * math.pi / 180) * speed
        self._pos_z -= math.sin(self._cam_angel * math.pi / 180) * speed
        # self._cam_pos.z += math.sin(self._cam_angel * math.pi / 180) * speed

    def rotate(self, angel):
        self._cam_angel = angel

    def get_postion(self) -> [float, float, float]:
        return [self._pos_x, self._pos_y, self._pos_z]

    def get_point_of_view(self) -> [float, float, float]:
        _x = self._pos_x + math.cos(self._cam_angel * math.pi / 180)
        _y = self._pos_y + math.cos(self._cam_angel_h * math.pi / 180)
        _z = self._pos_z + math.sin(self._cam_angel * math.pi / 180)
        print(self._cam_angel)
        return [_x, _y, _z]
