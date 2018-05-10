from laspy.file import File
import numpy as np
import scipy.spatial as spatial
import math
import pprint


class Node:
    x = 0
    y = 0
    z = 0
    shortest_dis = None
    neighbors = None

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Edge:
    startNode = None
    endNode = None
    weight = 0

    def __init__(self, m, n, w):
        self.startNode = m
        self.endNode = n
        self.weight = w


inFile = File('../filtered_points/filtered_points_0.5.las', mode='r')
points = np.transpose(np.array([inFile.x, inFile.y, inFile.z]))

# Put all points into a KdTree
point_tree = spatial.KDTree(points)

# print(inFile.header.max[0], inFile.header.max[1], inFile.header.max[2])

# find the boundary of the site;
boundary = np.array([[math.ceil(inFile.header.min[0]), math.ceil(inFile.header.min[1]), math.ceil(inFile.header.min[2])],
                    [math.floor(inFile.header.max[0]), math.floor(inFile.header.max[1]), math.floor(inFile.header.max[2])]])

print(boundary)

# set the closest distance to obstacles
c_dis = 2

# create a List to store nodes
nodes = [[[None for i in range(boundary[0, 0], boundary[1, 0])]
          for j in range(boundary[0, 1], boundary[1, 1])]
         for k in range(boundary[0, 2], boundary[1, 2])]

for i in range(boundary[0, 0], boundary[1, 0], c_dis):
    for j in range(boundary[0, 1], boundary[1, 1], c_dis):
        for k in range(boundary[0, 2], boundary[1, 2], c_dis):
            near_point = point_tree.query_ball_point([i, j, k], c_dis)
            # if obstacle within c_dis, do not create node
            if len(near_point) != 0:
                continue








