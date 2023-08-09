class Coordinate:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> [int, int]:
        return [self.x, self.y]
a = Coordinate(1, 2, 3)
print("a: ", a)