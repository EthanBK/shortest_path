from laspy.file import File
import numpy as np
import scipy.spatial as spatial
import math
import pprint
import random
from queue import PriorityQueue
import sys


class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        self.counter -= 1
        return item


def cvt_coord(index_list, dimension):
    res = index_list[0]
    res += index_list[1] * dimension[0]
    res += index_list[2] * dimension[0] * dimension[1]
    return res


def print_path(endIndex):
    prev = endIndex
    path = []
    while prev is not None:
        path.append(prev)
        prev = fromNode[prev]
    path.reverse()
    print("path index: ", path)


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


class Edge:
    def __init__(self, f, t, w):
        self.fromN = f
        self.endN = t
        self.weight = w
        self.direction = None


inFile = File('../filtered_points/filtered_points_2.5.las', mode='r')
points = np.transpose(np.array([inFile.x, inFile.y, inFile.z]))

# Put all points into a KdTree
point_tree = spatial.KDTree(points)

# print(inFile.header.max[0], inFile.header.max[1], inFile.header.max[2])

# find the boundary of the site;
boundary = np.array([[math.ceil(inFile.header.min[0]), math.ceil(inFile.header.min[1]), math.ceil(inFile.header.min[2])],
                    [math.floor(inFile.header.max[0]), math.floor(inFile.header.max[1]), math.floor(inFile.header.max[2])]])

print("boundary: ", boundary)
# Define parameters
c_dis = 20               # The closest distance to obstacles / the distance of nodes
weight_up = 2           # penalty to go up
weight_down = -1        # penalty to go down
weight_sharp_turn = 2   # penalty to take shape turn


# create a List to store nodes
nodes_list = [[[None for i in range(boundary[0, 2], boundary[1, 2], c_dis)]
               for j in range(boundary[0, 1], boundary[1, 1], c_dis)]
              for k in range(boundary[0, 0], boundary[1, 0], c_dis)]
dimension = [len(nodes_list), len(nodes_list[0]), len(nodes_list[0][0])]
print("dimension: ", dimension)

node_count = 0
distances = {}
visited = {}
unvisited = {}  # Create a dictionary
fromNode = {}

for i in range(boundary[0, 0], boundary[1, 0], c_dis):
    for j in range(boundary[0, 1], boundary[1, 1], c_dis):
        for k in range(boundary[0, 2], boundary[1, 2], c_dis):
            near_point = point_tree.query_ball_point([i, j, k], c_dis)
            # if obstacle within c_dis, do not create node
            if len(near_point) != 0:
                continue

            newNode = Node(i, j, k)
            newNode_index = [int((i - boundary[0, 0]) / c_dis),
                             int((j - boundary[0, 1]) / c_dis),
                             int((k - boundary[0, 2]) / c_dis)]
            newNode_index_linear = cvt_coord(newNode_index, dimension)
            distances[newNode_index_linear] = {}
            # print("New Node", newNode_index_linear)

            # Add neighbors
            for p in range(-1, 2):
                for q in range(-1, 2):
                    for r in range(-1, 2):
                        if p == 0 and q == 0 and r == 0:
                            continue
                            # create a list to store new index
                        nei_index = [newNode_index[0] + p,
                                     newNode_index[1] + q,
                                     newNode_index[2] + r]
                        if 0 <= nei_index[0] < dimension[0] and \
                                0 <= nei_index[1] < dimension[1] and \
                                0 <= nei_index[2] < dimension[2] and \
                                nodes_list[nei_index[0]][nei_index[1]][nei_index[2]] is not None:

                                # Calculate edge weight, right now only Euclidean distance
                                weight = math.sqrt(pow(p, 2) + pow(q, 2) + pow(r, 2)) * c_dis
                                nei_index_linear = cvt_coord(nei_index, dimension)
                                distances[newNode_index_linear][nei_index_linear] = weight
                                # print("neighbor", nei_index_linear, weight)
                                # newNode.neighbor.append([nei_index_linear, weight])
            nodes_list[newNode_index[0]][newNode_index[1]][newNode_index[2]] = newNode
            unvisited[newNode_index_linear] = None
            fromNode[newNode_index_linear] = None
            node_count += 1
print("node count", node_count)

# Set start point, range: x:0~402, y:0~700, z:0~61
sourceNode = None
x, y, z = 0, 0, 0
while sourceNode is None:
    x = int(random.random() * len(nodes_list))
    y = int(random.random() * len(nodes_list[0]))
    z = int(random.random() * len(nodes_list[0][0]))
    sourceNode = nodes_list[x][y][z]
sourceIndex = cvt_coord([x, y, z], dimension)
endNode = None
while endNode is None:
    x = int(random.random() * len(nodes_list))
    y = int(random.random() * len(nodes_list[0]))
    z = int(random.random() * len(nodes_list[0][0]))
    endNode = nodes_list[x][y][z]
endIndex = cvt_coord([x, y, z], dimension)

# error record
# success = [1581, 1493]
sourceIndex = 1581
endIndex = 1493
print("sourceIndex", sourceIndex)
print("endIndex", endIndex)

currentIndex = sourceIndex
currentWei = 0
unvisited[currentIndex] = currentWei


while True:
    for neighbor, weight in distances[currentIndex].items():
        if neighbor not in unvisited:
            continue
        newWeight = currentWei + weight
        if unvisited[neighbor] is None or unvisited[neighbor] > newWeight:
            unvisited[neighbor] = newWeight
            fromNode[neighbor] = currentIndex
    visited[currentIndex] = currentWei
    if currentIndex == endIndex:
        print("Short Path from Start to End is: ", currentWei)
        print_path(currentIndex)
        sys.exit("Path found!")
    del unvisited[currentIndex]
    if not unvisited:
        break

    candidates = [node for node in unvisited.items() if node[1]]
    if not candidates:
        sys.exit("No Path!")
    currentIndex, currentWei = sorted(candidates, key=lambda x: x[1])[0]


print(visited[endIndex])
print_path(endIndex)















