import math

class Point3D:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def dis_to(self, point):
        dis = math.sqrt(self.dis_square_to(point))
        return dis

    def dis_square_to(self, point):
        dis = (point.x - self.x) ** 2 + (point.y - self.y) ** 2 + (point.z - self.z) ** 2
        return dis

    def equals(self, point):
        if self.x == point.x and self.y ==point.y and self.z == point.z:
            return True
        else:
            return False

    def to_string(self):
        return '[' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ']'
