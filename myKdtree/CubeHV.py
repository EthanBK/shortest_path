import Point3D
import math


class CubeHV:
    xmax = 0
    xmin = 0
    ymax = 0
    ymin = 0
    zmax = 0
    zmin = 0

    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.xmin = x1
        self.xmax = x2
        self.ymin = y1
        self.ymax = y2
        self.zmin = z1
        self.zmax = z2

    def contains(self, point):
        if self.xmin <= point.x and self.xmax >= point.x and \
                self.ymin <= point.y and self.ymax >= point.y and \
                self.zmin <= point.z and self.zmax >= point.z:
            return True
        else:
            return False

    def contained_by_ball(self, point, radius):
        if point.x > (self.xmin + self.xmax) / 2:
            x = self.xmin
        else:
            x = self.xmax
        if point.y > (self.ymin + self.ymax) / 2:
            y = self.ymin
        else:
            y = self.ymax
        if point.z > (self.zmin + self.zmax) / 2:
            z = self.zmin
        else:
            z = self.zmax

        distance = math.sqrt((x - point.x) ** 2 + (y - point.y) ** 2 + (z - point.z) ** 2)
        return distance <= radius

    def intersect(self, point, radius):
        x = max(self.xmin, min(point.x, self.xmax))
        y = max(self.ymin, min(point.y, self.ymax))
        z = max(self.zmin, min(point.z, self.zmax))
        distance = math.sqrt((x - point.x) ** 2 + (y - point.y) ** 2  + (z - point.z) ** 2)
        return distance <= radius

    def to_string(self):
        return [[self.xmin, self.ymin, self.zmin],
                [self.xmax, self.ymax, self.zmax]]