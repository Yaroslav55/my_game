from render import Render, Vector3f

class Scene(object):

    def __init__(self, render_Obj : Render):
        self._render = render_Obj

        self.scene_state = {"isTerrainCreated": 0}
        self.vertex_array = [[0] * 3 for i in range(5 * 5)]
        self.index_array = []
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
    def _make_terrain(self, hight, width):
        # index_buffer = (1, 6, 2, 7, 3, 8, 4, 9, 5, 10, 10, 6, 6, 11, 7, 12, 8, 13, 9, 14, 10, 15)
        # vertex_arr: list[list[float]] = [
        #     [3, 5, 0], [4, 5, 0], [5, 5, 0], [6, 5, 0], [7, 5, 0],
        #     [3, 4, 0], [4, 4, 0], [5, 4, 0], [6, 4, 0], [7, 4, 0],
        #     [3, 3, 0], [4, 3, 0], [5, 3, 0], [6, 3, 0], [7, 3, 0]
        # ]
        offset = 1
        row = 0
        for i in range(hight):
            for j in range(width):
                self.vertex_array[j + row][0] = j
                self.vertex_array[j + row][1] = i
                self.vertex_array[j + row][2] = 0
            row += hight
        for i in range(hight * width - (hight - 1))[1::]:
            if i == 1:
                self.index_array.append(1)
            if i % hight == 0:
                #       Always will be one extra degenerate triangle
                self.index_array.append(i + width)
                self.index_array.append(i + width)
                self.index_array.append(i + 1)
                self.index_array.append(i + 1)
            else:
                self.index_array.append(i + width)
                self.index_array.append(i + 1)

            #           BULLSHITTT !
            self._render.vertex_array = self.vertex_array
            self._render.index_array = self.index_array

    def draw_terrain(self, hight, width):
        if not self.scene_state["isTerrainCreated"]:
            self._make_terrain(hight, width)
            self.scene_state = 0

