from laspy.file import File
import numpy as np

class Node:
    x = 0
    y = 0
    z = 0
    neighbors = None

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

inFile = File('../filtered_points/filtered_points_0.5.las', mode='r')
points = np.transpose(np.array([inFile.x, inFile.y, inFile.z]))

# find the boundary of the site;
boundary  = np.array([inFile.header.min.x, inFile.header.min.y, inFile.header.min.z],
                     [inFile.header.max.x, inFile.header.max.y, inFile.header.max.z])

# set the closest distance to obstacles
c_dis = 2

for i in range(boundary[0, 0], boundary[1, 0], c_dis):
    for j in range(boundary[0, 1], boundary[1, 1], c_dis):
        for k in range(boundary[0, 2], boundary[1, 2], c_dis):
            node = Node(i, j, k)


