import math
from scene import Mesh

class Camera3D(object):
    CAMERA_SPEED = 4
    CAMERA_ANGEL = 5

    def __init__(self, pos_x, pos_y, pos_z, angle=-90, angle_top=90):
        self.cam_angel = angle
        self.cam_angel_h = angle_top  # Angel for 3D scene
        # self.cam_angel_h = 180
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._pos_z = pos_z
        self.player_mesh: Mesh
    def set_player_mesh(self, model : Mesh):
        self.player_mesh = model
    def move_forward(self, angle = CAMERA_ANGEL, speed=CAMERA_SPEED):
        self._pos_x += math.cos(self.cam_angel * math.pi / 180) * speed
        self._pos_z += math.sin(self.cam_angel * math.pi / 180) * speed

    def move_back(self, angle = CAMERA_ANGEL, speed=CAMERA_SPEED):
        self._pos_x -= math.cos(self.cam_angel * math.pi / 180) * speed
        self._pos_z -= math.sin(self.cam_angel * math.pi / 180) * speed
        self.player_mesh.directionOfMovement.set_variables(self._pos_x, self._pos_y, self._pos_z)
        self.player_mesh.directionOfMovement.z += 30
    def move_up(self, speed=CAMERA_SPEED):
        self._pos_y += speed

    def move_down(self, speed=CAMERA_SPEED):
        self._pos_y -= speed

    def move_left(self, speed=CAMERA_SPEED, angle=CAMERA_ANGEL):
        self._rotate_XZ(angle)

    def move_right(self, speed=CAMERA_SPEED, angle=CAMERA_ANGEL):
        self._rotate_XZ(-angle)

    def _rotate_XZ(self, angel):
        if self.cam_angel == 360 or self.cam_angel == -360:
            self.cam_angel = 0
        else:
            self.cam_angel -= angel

    def rotate_Y(self, angle):
        if self.cam_angel_h == 360 or self.cam_angel_h == -360:
            self.cam_angel_h = 0
        else:
            self.cam_angel_h -= angle

    def get_postion(self) -> [float, float, float]:
        return [self._pos_x, self._pos_y, self._pos_z]

    def get_point_of_view(self) -> [float, float, float]:
        _x = self._pos_x + math.cos(self.cam_angel * math.pi / 180)
        _y = self._pos_y + math.cos(self.cam_angel_h * math.pi / 180)
        _z = self._pos_z + math.sin(self.cam_angel * math.pi / 180)
        return [_x, _y, _z]


class Camera2D(Camera3D):
    CAMERA_SPEED = 4
    CAMERA_ANGEL = 5

    def __init__(self, pos_x, pos_y, pos_z, angle=-90, angle_top=90):
        super().__init__(pos_x, pos_y, pos_z, angle, angle_top)

    def move_left(self, angle=CAMERA_ANGEL, speed=CAMERA_SPEED):
        self._pos_z -= speed

    def move_right(self, angle=CAMERA_ANGEL, speed=CAMERA_SPEED):
        self._pos_z += speed

    def rotate_Y(self, angle):
        # if self.cam_angel_h == 360 or self.cam_angel_h == -360:
        #     self.cam_angel_h = 0
        # else:
        print(self.cam_angel_h)
        self.cam_angel_h -= angle

    def get_point_of_view(self) -> [float, float, float]:
        _x = self._pos_x + math.cos(self.cam_angel * math.pi / 180)
        # _y = self._pos_y + math.cos(self.cam_angel_h * math.pi / 180)
        _y = self._pos_y - 1
        _z = self._pos_z + math.sin(self.cam_angel * math.pi / 180)
        return [_x, _y, _z]
