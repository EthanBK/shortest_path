import Point3D
import math
from CubeHV import CubeHV
import queue


class Node:
    id = None
    point = None
    lbb = None
    rtf = None
    direction = None
    is_deleted = None
    cube = None

    def __init__(self, id, point, cube, direction):
        self.id = id
        self.point = point
        self.direction = direction
        self.is_deleted = False
        self.cube = cube


class KdTree:

    root = None
    size = 0

    def __init__(self):
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def get_size(self):
        print(self.size)
        return self.size

    def insert(self, id, point):
        self.root = self.insert_node(id, self.root, None, point, 0)

    def insert_node(self, id, node, parent, point, compare):

        if node is None:
            if self.size == 0:
                self.size += 1

                # print(id, point.to_string())
                # print(cube.to_string())
                return Node(id, point, None, 0)
            self.size += 1

            return Node(id, point, None, (parent.direction + 1) % 3)

        cmp = self.compare(point, node.point, node.direction)
        if cmp < 0:
            node.lbb = self.insert_node(id, node.lbb, node, point, cmp)
        elif cmp >= 0:
            node.rtf = self.insert_node(id, node.rtf, node, point, cmp)

        return node

    def delete(self, node):
        node.is_delete = True

    def nearest(self, point):
        if point is None:
            print("Invalid Query Point")

        if self.root is None:
            return None
        return self.nearest_tool(self.root, self.root.point, point)

    def nearest_tool(self, node, nearest, point):

        if node is None:
            return nearest

        if point.dis_square_to(node.point) < point.dis_square_to(nearest):
            nearest = node.point

        cmp = self.compare(point, node.point, node.direction)

        if cmp < 0:
            nearest = self.nearest_tool(node.lbb, nearest, point)
            if node.rtf is not None:
                if self.cube_square_dis(node, point) < point.dis_square_to(nearest):
                    nearest = self.nearest_tool(node.rtf, nearest, point)

        if cmp > 0:
            nearest = self.nearest_tool(node.rtf, nearest, point)
            if node.lbb is not None:
                if self.cube_square_dis(node, point) < point.dis_square_to(nearest):
                    nearest = self.nearest_tool(node.lbb, nearest, point)

        return nearest

    def compare(self, p1, p2, direction):

        if p1.equals(p2):
            return 0

        cmp = None
        if direction == 0:
            if p1.z > p2.z:
                cmp = 1
            else:
                cmp = -1

        elif direction == 1:
            if p1.y > p2.y:
                cmp = 1
            else:
                cmp = -1

        elif direction == 2:
            if p1.x > p2.x:
                cmp = 1
            else:
                cmp = -1
        else:
            print("Distance Error in compare")

        return cmp

    def cube_square_dis(self, node, point):
        if node is None:
            return
        if node.direction == 0:
            return abs(node.point.z - point.z) ** 2
        elif node.direction == 1:
            return abs(node.point.y - point.z) ** 2
        elif node.direction == 2:
            return abs(node.point.x - point.x) ** 2
        else:
            print("Distance Error in cube_dis")
            return None

    def nearest_dis(self, point):
        return point.dis_to(self.nearest(point))

    def radius_query(self, point, dis):
        if point is None:
            print("Point is None!")
        res = []
        return self.radius_query_tool(self.root, res, point, dis)

    def radius_query_tool(self, node, res, point, dis):
        if node is None:
            return res
        if node.cube.contained_by_ball(point, dis):
            self.push_all(res, node)
        else:
            if (not node.is_deleted) and point.dis_to(node.point) <= dis:
                res.append(node.id)
                node.is_deleted = True

            if node.lbb is not None and \
                  node.lbb.cube.intersect(point, dis):
                res = self.radius_query_tool(node.lbb, res, point, dis)
            if node.rtf is not None and \
                  node.rtf.cube.intersect(point, dis):
                res = self.radius_query_tool(node.rtf, res, point, dis)
        return res

    def push_all(self, res, node):
        if node is None:
            return
        else:
            if not node.is_deleted:
                res.append(node.id)
                node.is_deleted = True
            self.push_all(res, node.lbb)
            self.push_all(res, node.rtf)

    def visualize_tree(self):
        q = queue.Queue(maxsize=0)
        q.put(self.root)
        while not q.empty():
            len = q.qsize()
            line = ''
            for i in range(len):
                cur = q.get()
                line += (cur.point.to_string() + ' ')
                if cur.lbb is not None:
                    q.put(cur.lbb)
                else:
                    line += 'none '
                if cur.rtf is not None:
                    q.put(cur.rtf)
                else:
                    line += 'none '
            print(line)

    # def delete_node(self, point):
    #     if point is None:
    #         raise('None point delete error!')
    #     self.root = self.delete_tool(self.root, point)
    #
    # def delete_tool(self, node, point):
    #     if node.cube.contains(point):
    #         # if the node to be delete has no child
    #         if node.point.equals(point):
    #             if node.lbb is None and node.rtf is None:
    #                 return None
    #
    #             elif node.rtf is not None:
    #                 node = find_min(node, node, )
    #
    #
    #     else:
    #
    #
    # def find_min_dim(self, node, minNode):
    #     if node is None:
    #         return minNode
    #
    #     if node.direction == 0:






