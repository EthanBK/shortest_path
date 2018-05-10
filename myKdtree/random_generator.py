import numpy as np
from Point3D import Point3D
from KdTree import KdTree
import progressbar
import random

# A progress bar to show the progress of execution
bar = progressbar.ProgressBar(widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',
])

for i in range(10):
    pass

# Initialize Kd-Tree
kdt = KdTree()
len_input = 20000000 # About the same length as the .las file
max = 100000
min = 0
threshold = 100
print("Initial Length: ", len_input)


# For each point in data set, get the nearest distance
# first, then check if the distance is bigger then the \
# threshold, if yes, insert point into kd-Tree
def get_random_point():
    in_x = random.random() * max
    in_y = random.random() * max
    in_z = random.random() * max
    return Point3D(in_x, in_y, in_z)

    # if not kdt.is_empty():
    #     if kdt.nearest_dis(point) < threshold:
    #         kdt.insert(point)
    # kdt.insert(point)

len_output = len(outFile.points)

# print("Number of Entries Left: ", len_output)
# print("File size has been reduced %.2f %", (len_input - len_output)/len_input)

for i in bar(range(len_input)):
    if flag[i] == 1:
        pi = Point3D(points[0, i], points[1, i], points[2, i])
        for j in bar(range(i + 1, len_input)):
            if flag[j] == 1:
                pj = Point3D(points[0, j], points[1, j], points[2, j])
                dis = pj.dis_to(pi)
                if dis <= threshold:
                    flag[j] = 0
        point_keep.append(i)








