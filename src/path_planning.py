from laspy.file import File
import numpy as np
import scipy.spatial as spatial
import math
import random
import dijkstra_path_planning as dpp
from potential_field_path_planning import PFPP
import sys


def print_path(end_index, from_node, method):
    prev = end_index
    path = []
    while prev is not None:
        path.append(prev)
        prev = from_node[prev]
    path.reverse()
    print("path index: ", path)
    if method == "dpp":
        with open('../data/path_dpp.txt', 'w') as fp:
            for item in path:
                fp.write("%s," % item)
    if method == "pfpp":
        with open('../data/path_pfpp.txt', 'w') as fp:
            for item in path:
                fp.write("%s," % item)


def cvt_coord_to_line(index_list, dimension):
    res = index_list[0]
    res += index_list[1] * dimension[0]
    res += index_list[2] * dimension[0] * dimension[1]
    return res


def build_grid(parameter):

    c_dis, weight_up, weight_down, weight_turn = parameter

    # read las data
    in_file = File('../filtered_points/filtered_points_0.5.las', mode='r')
    points = np.transpose(np.array([in_file.x, in_file.y, in_file.z]))

    # Build KDTree
    point_tree = spatial.KDTree(points)

    # find the boundary of the site;
    boundary = np.array(
        [[math.ceil(in_file.header.min[0]), math.ceil(in_file.header.min[1]), math.ceil(in_file.header.min[2])],
         [math.floor(in_file.header.max[0]), math.floor(in_file.header.max[1]), math.floor(in_file.header.max[2])]])

    # create a List to store nodes
    nodes_list = [[[None for i in range(boundary[0, 2], boundary[1, 2], c_dis)]
                   for j in range(boundary[0, 1], boundary[1, 1], c_dis)]
                  for k in range(boundary[0, 0], boundary[1, 0], c_dis)]
    dimension = [len(nodes_list), len(nodes_list[0]), len(nodes_list[0][0])]
    with open('../data/dimension.txt', 'w') as fp:
        for item in dimension:
            fp.write('%s,' % item)

    return nodes_list, dimension, boundary, point_tree


# calculate or read start and end point
def get_start_end(dimension, create_new_start):
    sx, sy, sz, ex, ey, ez = 0, 0, 0, 0, 0, 0
    if not create_new_start:
        with open("../data/start_end.txt", 'r') as fp:
            source_index, end_index = fp.read().split(',')
            source_index = int(source_index)
            end_index = int(end_index)
    else:
        # Set start point, range: x:0~402, y:0~700, z:0~61
        source_node = None
        while source_node is None:
            sx = int(random.random() * dimension[0])
            sy = int(random.random() * dimension[1])
            sz = int(random.random() * dimension[2])
        end_node = None
        while end_node is None:
            ex = int(random.random() * dimension[0])
            ey = int(random.random() * dimension[1])
            ez = int(random.random() * dimension[2])
        end_index = cvt_coord_to_line([ex, ey, ez], dimension)
        source_index = cvt_coord_to_line([sx, sy, sz], dimension)
        with open('../data/start_end.txt', 'a') as fp:
            fp.write('%s, %s', source_index, end_index)
    return [source_index, end_index]


def main():
    # Define parameters
    c_dis = 10  # The closest distance to obstacles / the distance of nodes
    weight_up = 2  # penalty to go up
    weight_down = -1  # penalty to go down
    weight_turn = 2  # penalty to take shape turn
    parameter = [c_dis, weight_up, weight_down, weight_turn]
    create_new_start = False

    # Build Grid in the space
    nodes_list, dimension, boundary, point_tree = build_grid(parameter)
    print("Build Grid Finish!")
    print("boundary:\n", boundary)
    print("dimension:\n", dimension)

    # Get start and end points
    print("Generating Start and End points...")
    start_end = get_start_end(dimension, create_new_start)
    print("Complete!", start_end)

    # Implement Dijkstra's Algorithm to find shortest path
    end_index_dpp, from_node_dpp, path_length = dpp.dijk(dimension, boundary, point_tree, nodes_list, start_end)
    print("Path Found by Dijkstra's Shortest Path:")
    print_path(end_index_dpp, from_node_dpp, "dpp")
    print("Path Length: ", path_length)

    # Implement Potential Field Path Planning
    pfpp = PFPP()
    end_index_pfpp, from_node_pfpp, path_length = pfpp.main(nodes_list, dimension, boundary, start_end, point_tree, c_dis)
    print("Path Found by Potential Field PP:")
    print_path(end_index_pfpp, from_node_pfpp, "pfpp")
    print("Path Length: ", path_length)


if __name__ == '__main__':
    main()

