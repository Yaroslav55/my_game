from render import Render, Vector3f


class Scene(object):

    def __init__(self):
        self._render = Render()

    def draw_grid(self):
        _pos_1 = Vector3f(0.0, 0.0, 0.0)
        _pos_2 = Vector3f(0.0, 0.0, 0.0)
        _color = Vector3f(0.0, 1.0, 1.0)
        grid_size = 20

        for i in range(60):
            _pos_1.set_variables(-10, -1, i - 30)
            _pos_2.set_variables(-10 + grid_size, -1, i - 30)
            self._render.make_line(_pos_1, _pos_2, _color)

            _pos_1.set_variables(i - 30, -1, -10)
            _pos_2.set_variables(i - 30, -1, -10 + grid_size)
            self._render.make_line(_pos_1, _pos_2, _color)

    def draw_terrain(self):
        pass