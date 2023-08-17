
import math

class Camera(object):
    CAMERA_SPEED = 4
    CAMERA_ANGEL = 5
    def __init__(self, pos_x, pos_y, pos_z, angle=0, angle_top=90):
        self.cam_angel = angle
        self.cam_angel_h = angle_top  # Angel for 3D scene
        # self.cam_angel_h = 180
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._pos_z = pos_z

    def move_forward(self, angle, speed = CAMERA_SPEED):
        self._pos_x += math.cos(self.cam_angel * math.pi / 180) * speed
        self._pos_z += math.sin(self.cam_angel * math.pi / 180) * speed
        # self._cam_pos.z += math.sin(self._cam_angel * math.pi / 180) * speed

    def move_back(self, angle, speed = CAMERA_SPEED):
        self._pos_x -= math.cos(self.cam_angel * math.pi / 180) * speed
        self._pos_z -= math.sin(self.cam_angel * math.pi / 180) * speed
        #self._pos_y = math.sin(self._cam_angel_h * math.pi / 180) * speed
    def move_up(self, speed):
        self._pos_y += speed
    def move_down(self, speed):
        self._pos_y -= speed
    def rotate(self, angel, angel_y = 90):
        if angel == 360 or angel == -360:
            self.cam_angel = 0
        else:
            self.cam_angel = angel
        self._cam_angel_h = angel_y

    def get_postion(self) -> [float, float, float]:
        return [self._pos_x, self._pos_y, self._pos_z]

    def get_point_of_view(self) -> [float, float, float]:
        _x = self._pos_x + math.cos(self.cam_angel * math.pi / 180)
        _y = self._pos_y + math.cos(self.cam_angel_h * math.pi / 180)
        _z = self._pos_z + math.sin(self.cam_angel * math.pi / 180)
        return [_x, _y, _z]
