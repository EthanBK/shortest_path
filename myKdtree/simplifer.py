from laspy.file import File
import numpy as np
import itertools
from Point3D import Point3D
from KdTree import KdTree
import progressbar
import multiprocessing as mp

# Read in .las file as inFile
inFile = File('fn.las', mode='r')
# pointformat = inFile.point_format
# for spec in inFile.point_format:
#     print("point: ", spec.name)
# print(inFile.points[0])
#
# headerformat = inFile.header.header_format
# for spec in headerformat:
#     print("header: ", spec.name)

# Create output file.las
outFile = File("../data/filtered_points.las", mode = "w", header = inFile.header)
# Create list for storing the index of kept points
point_keep = []

# Pre-load .las into numpy array
points = np.array([inFile.x, inFile.y, inFile.z])
len_input = points.shape[1]
# Mark the delete with 0 in flag[]
flag = np.ones(len_input)

# A progress bar to show the progress of execution
bar = progressbar.ProgressBar(widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',
])

# Set threshold: the min distance
threshold = 1
dis_sum = 0
#
# Initialize Kd-Tree
kdt = KdTree()
print("Initial Length: ", len_input)

#solution 2:
# for all p ∈ point cloud do
#   for all n∈ point cloud such that ∥n−p∥<=d do
#       delete n
#   end for
# end for
for i in bar(range(len_input)):
    if flag[i] == 1:
        pi = Point3D(points[0, i], points[1, i], points[2, i])
        for j in range(i + 1, len_input):
            if flag[j] == 1:
                pj = Point3D(points[0, j], points[1, j], points[2, j])
                dis = pj.dis_to(pi)
                if dis <= threshold:
                    # print("j = ", j, "dis = ", dis)
                    flag[j] = 0
        point_keep.append(i)
        # print("i = ", i)

len_output = len(point_keep)

print("Number of Entries Left: ", len_output)
print("File size has been reduced %.2f %", (len_input - len_output)/len_input)
