import math
import numpy as np

class PFPP:

    # Define parameters
    KP = 5.0        # Attractive potential gain
    ETA = 100.0     # repulsive potential gain
    start_index = 0
    end_index = 0
    nodes_list = []
    dimension = []
    boundary = []
    point_tree = None
    c_dist = 0      # Density of grid
    safe_dist = 5   # closest distance to obstacle

    def cvt_coord_to_cube(self, index):
        res = []
        res.append(index // (self.dimension[0] * self.dimension[1]))
        index -= res[0] * self.dimension[0] * self.dimension[1]
        res.append(index // self.dimension[0])
        index -= res[1] * self.dimension[0]
        res.append(index)
        res.reverse()
        return res

    def cvt_coord_to_line(self, index_cub):
        res = index_cub[0]
        res += index_cub[1] * self.dimension[0]
        res += index_cub[2] * self.dimension[0] * self.dimension[1]
        return res

    def cal_attractive_potential(self, x_ind, y_ind, z_ind):
        gx, gy, gz = self.cvt_coord_to_cube(self.end_index)
        dist_to_end = self.c_dist * math.sqrt((x_ind - gx) ** 2 + (y_ind - gy) ** 2 + (z_ind - gz) ** 2)
        return 0.5 * self.KP * dist_to_end

    def cal_repulsive_potential(self, x_ind, y_ind, z_ind, dis_map):
        # get distance to the nearest obstacle
        dist_to_obstacle = dis_map[x_ind][y_ind][z_ind]
        # calculate repulsive potential
        if dist_to_obstacle <= self.safe_dist:
            if dist_to_obstacle < 0.1:
                dist_to_obstacle = 0.1
            re_po = 0.5 * self.ETA * (1.0 / dist_to_obstacle - 1.0 / self.safe_dist) ** 2
        else:
            re_po = 0
        return re_po

    # calculate the potential map
    def calculate_potential_field_map(self, dis_map):
        potential_map = np.empty(self.dimension, dtype=object)
        for i in range(self.dimension[0]):
            for j in range(self.dimension[0]):
                for k in range(self.dimension[0]):
                    attr_po = self.cal_attractive_potential(i, j, k)
                    rep_po = self.cal_repulsive_potential(i, j, k, dis_map)
                    po = attr_po + rep_po
                    potential_map[i][j][k] = po
        return potential_map

    # Using KdTree to calculate the nearest distance from each point to obstacle
    def get_near_dis_map(self):
        coord_map = np.empty(self.dimension, dtype=object)
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                for k in range(self.dimension[2]):
                    coord_map[i][j][k] = [self.boundary[0][0] + i * self.c_dist,
                                          self.boundary[0][1] + j * self.c_dist,
                                          self.boundary[0][2] + k * self.c_dist]
        dis_map = self.point_tree.query(coord_map)
        return dis_map

    def potential_field_planning(self):
        # Define parameters
        from_node = []
        dis_map = self.get_near_dis_map()
        potential_map = self.calculate_potential_field_map(dis_map)
        # todo: find path based on potential_map, store the path in from_node
        gx, gy, gz = self.cvt_coord_to_cube(self.end_index)
        cx, cy, cz = self.cvt_coord_to_cube(self.start_index)
        dist_to_end = self.c_dist * math.sqrt((cx - gx) ** 2 + (cy - gy) ** 2 + (cz - gz) ** 2)
        next_step = [[-1, 0, 1],
                     [-1, 0, 1],
                     [-1, 0, 1]]

        while dist_to_end < self.c_dist:
            mind = float("inf")
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    for k in range(-1, 2, 1):
                        nei_x, nei_y, nei_z = [cx + i, cy + j, cz + k]
                        if nei_x < 0 or nei_x > self.dimension[0] or \
                           nei_y < 0 or nei_y > self.dimension[1] or \
                           nei_z < 0 or nei_z > self.dimension[2]:
                            continue


        return from_node

    def main(self, nodes_list, dimension, boundary, start_end, point_tree, c_dis):
        print("Start Potential Field Path Planning")
        self.nodes_list = nodes_list
        self.dimension = dimension
        self.boundary = boundary
        self.point_tree = point_tree
        self.c_dist = c_dis
        # read start and end point
        self.start_index, self.end_index = start_end
        from_node = self.potential_field_planning()
        return from_node

