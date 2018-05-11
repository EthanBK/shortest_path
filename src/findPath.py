from laspy.file import File
import numpy as np
import scipy.spatial as spatial
import math
import pprint
import random
from queue import PriorityQueue


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


q = MyPriorityQueue()
q.put("itme1", 1)
q.put("itme2", 2)
q.put("itme5", 5)
q.put("itme4", 4)


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


inFile = File('../filtered_points/filtered_points_0.5.las', mode='r')
points = np.transpose(np.array([inFile.x, inFile.y, inFile.z]))

# Put all points into a KdTree
point_tree = spatial.KDTree(points)

# print(inFile.header.max[0], inFile.header.max[1], inFile.header.max[2])

# find the boundary of the site;
boundary = np.array([[math.ceil(inFile.header.min[0]), math.ceil(inFile.header.min[1]), math.ceil(inFile.header.min[2])],
                    [math.floor(inFile.header.max[0]), math.floor(inFile.header.max[1]), math.floor(inFile.header.max[2])]])

print("boundary: ", boundary)
# Define parameters
c_dis = 5               # The closest distance to obstacles / the distance of nodes
weight_up = 2           # penalty to go up
weight_down = -1        # penalty to go down
weight_sharp_turn = 2   # penalty to take shape turn


# create a List to store nodes
nodes_list = [[[None for i in range(boundary[0, 2], boundary[1, 2], c_dis)]
               for j in range(boundary[0, 1], boundary[1, 1], c_dis)]
              for k in range(boundary[0, 0], boundary[1, 0], c_dis)]
print("nodes_size: ", len(nodes_list), " x ", len(nodes_list[0]), " x ", len(nodes_list[0][0]))

node_count = 0
unvisited = MyPriorityQueue()

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
            # print("new node", newNode.coord())
            # Add neighbors
            for p in range(-1, 2):
                for q in range(-1, 2):
                    for r in range(-1, 2):
                        if p == 0 and q == 0 and r == 0:
                            continue
                        nei_index = [newNode_index[0] + p,
                                     newNode_index[1] + q,
                                     newNode_index[2] + r]
                        if 0 <= nei_index[0] < len(nodes_list) and \
                                0 <= nei_index[1] < len(nodes_list[0]) and \
                                0 <= nei_index[2] < len(nodes_list[0][0]) and \
                                nodes_list[nei_index[0]][nei_index[1]][nei_index[2]] is not None:
                                # Calculate edge weight, right now only Euclidean distance
                                weight = math.sqrt(pow(p, 2) + pow(q, 2) + pow(r, 2)) * c_dis
                                # print(nodes_list[nei_index[0]][nei_index[1]][nei_index[2]].coord(), weight)
                                newNode.neighbor.append([[nei_index[0], nei_index[1], nei_index[2]], weight])
            nodes_list[newNode_index[0]][newNode_index[1]][newNode_index[2]] = newNode
            unvisited.put(newNode_index, newNode.dist)
            node_count += 1

# Set start point, range: x:0~402, y:0~700, z:0~61
sourceNode = None
while sourceNode is None:
    x = random.random() * len(nodes_list)
    y = random.random() * len(nodes_list[0])
    z = random.random() * len(nodes_list[0][0])
    sourceNode = nodes_list[x][y][z]

# calculate shortest  distance from source
# while not unvisited.empty():
#     u = unvisited.get()
#     for i in range(len(u.neighbor)):
#         nei = u.neighbor[i]
#         alt = u.dist + nei[1]

print(node_count)










