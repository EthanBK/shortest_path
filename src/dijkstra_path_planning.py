from laspy.file import File
import numpy as np
import scipy.spatial as spatial
import math
import random
from queue import PriorityQueue
import sys


def cvt_coord_to_line(index_list, dimension):
    res = index_list[0]
    res += index_list[1] * dimension[0]
    res += index_list[2] * dimension[0] * dimension[1]
    return res


def cvt_coord_to_cube(index, dimension):
    res = []
    res.append(index // (dimension[0] * dimension[1]))
    index -= res[0] * dimension[0] * dimension[1]
    res.append(index // dimension[0])
    index -= res[1] * dimension[0]
    res.append(index)
    res.reverse()
    return res


class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.neighbor = []
        self.dist = math.inf
        self.visited = False
        self.velocity_victor = None
        self.pre = None

    def coord(self):
        return [self.x, self.y, self.z]


# inFile = File('../filtered_points/filtered_points_0.5.las', mode='r')
# points = np.transpose(np.array([inFile.x, inFile.y, inFile.z]))
#
# # Put all points into a KdTree
# point_tree = spatial.KDTree(points)

# print(inFile.header.max[0], inFile.header.max[1], inFile.header.max[2])

# # find the boundary of the site;
# boundary = np.array([[math.ceil(inFile.header.min[0]), math.ceil(inFile.header.min[1]), math.ceil(inFile.header.min[2])],
#                     [math.floor(inFile.header.max[0]), math.floor(inFile.header.max[1]), math.floor(inFile.header.max[2])]])
# print("boundary: ", boundary)

# Define parameters
c_dis = 10               # The closest distance to obstacles / the distance of nodes
weight_up = 2           # penalty to go up
weight_down = -1        # penalty to go down
weight_sharp_turn = 2   # penalty to take shape turn


# # create a List to store nodes
# nodes_list = [[[None for i in range(boundary[0, 2], boundary[1, 2], c_dis)]
#                for j in range(boundary[0, 1], boundary[1, 1], c_dis)]
#               for k in range(boundary[0, 0], boundary[1, 0], c_dis)]
# dimension = [len(nodes_list), len(nodes_list[0]), len(nodes_list[0][0])]
# with open('../data/dimension.txt', 'w') as fp:
#     for item in dimension:
#         fp.write('%s,' % item)
# print("dimension: ", dimension)

def build_grpah(boundary, dimension, nodes_list, point_tree):

    node_count = 0
    distances = {}
    visited = {}
    unvisited = {}  # Create a dictionary
    from_node = {}

    for i in range(boundary[0, 0], boundary[1, 0], c_dis):
        for j in range(boundary[0, 1], boundary[1, 1], c_dis):
            for k in range(boundary[0, 2], boundary[1, 2], c_dis):
                near_point = point_tree.query_ball_point([i, j, k], c_dis)
                # if obstacle within c_dis, do not create node
                if len(near_point) != 0:
                    continue

                new_node = Node(i, j, k)
                new_node_index = [int((i - boundary[0, 0]) / c_dis),
                                  int((j - boundary[0, 1]) / c_dis),
                                  int((k - boundary[0, 2]) / c_dis)]
                new_node_index_linear = cvt_coord_to_line(new_node_index, dimension)
                distances[new_node_index_linear] = {}
                # print("New Node", newNode_index_linear)

                # Add neighbors
                for p in range(-1, 2):
                    for q in range(-1, 2):
                        for r in range(-1, 2):
                            if p == 0 and q == 0 and r == 0:
                                continue
                                # create a list to store new index
                            nei_index = [new_node_index[0] + p,
                                         new_node_index[1] + q,
                                         new_node_index[2] + r]
                            if 0 <= nei_index[0] < dimension[0] and \
                               0 <= nei_index[1] < dimension[1] and \
                               0 <= nei_index[2] < dimension[2] and \
                               nodes_list[nei_index[0]][nei_index[1]][nei_index[2]] is not None:
                                # Calculate edge weight, right now only Euclidean distance
                                weight = math.sqrt(pow(p, 2) + pow(q, 2) + pow(r, 2)) * c_dis
                                nei_index_linear = cvt_coord_to_line(nei_index, dimension)
                                distances[new_node_index_linear][nei_index_linear] = weight
                                # print("neighbor", nei_index_linear, weight)
                                # newNode.neighbor.append([nei_index_linear, weight])
                nodes_list[new_node_index[0]][new_node_index[1]][new_node_index[2]] = new_node
                unvisited[new_node_index_linear] = None
                from_node[new_node_index_linear] = None
                node_count += 1
    print("node count", node_count)
    return distances, visited, unvisited, from_node


def dijk(dimension, boundary, point_tree, nodes_list, start_end):
    distances, visited, unvisited, from_node = build_grpah(boundary, dimension, nodes_list, point_tree)

    source_index, end_index = start_end

    current_index = source_index
    current_wei = 0
    unvisited[current_index] = current_wei

    while True:
        for neighbor, weight in distances[current_index].items():
            if neighbor not in unvisited:
                continue
            new_weight = current_wei + weight
            if unvisited[neighbor] is None or unvisited[neighbor] > new_weight:
                unvisited[neighbor] = new_weight
                from_node[neighbor] = current_index
        visited[current_index] = current_wei
        if current_index == end_index:
            print("Short Path Distance from Start to End is: ", current_wei)
            return current_index, from_node

            # print_path(current_index, from_node)

        del unvisited[current_index]
        if not unvisited:
            break

        candidates = [node for node in unvisited.items() if node[1]]
        if not candidates:
            sys.exit("No Path!")
        current_index, current_wei = sorted(candidates, key=lambda x: x[1])[0]
    return end_index, from_node
    # print(visited[end_index])














