from Point3D import Point3D
from KdTree import KdTree
import numpy as np
import timeit
from laspy.file import File
import itertools
import random

min_dis = 1

stats = open('../data/test_insert.csv', 'w')
header = "id,num_insert,time" + '\n'
stats.write(header)

# .las file read and write
inFile = File('fn.las', mode='r')
# Pre-load .las into numpy array
points = np.transpose(np.array([inFile.x, inFile.y, inFile.z]))
# len_input = points.shape[0]
len_input_start = 100000
len_input_end = 10000000
max_value = 2000000
# insert points into kd-tree


for t in itertools.count():
    len = len_input_start * t
    t1 = timeit.default_timer()
    myKdt = KdTree()
    for i in range(len):
        in_x = random.random() * max
        in_y = random.random() * max
        in_z = random.random() * max
        p = Point3D(in_x, in_y, in_z)
        # p = Point3D(points[i, 0], points[i, 1], points[i, 2])
        myKdt.insert(i, p)

    t2 = timeit.default_timer()
    stats = open('../data/test_insert.csv', 'a')
    line = str(t) + ',' + str(len) + ',' + str(t2 - t1) + '\n'
    stats.write(line)
    stats.close()
    print("Insertion Complete. Time: ", t2 - t1)


# for l in itertools.count():
#     time_start = timeit.default_timer()
#     min_dis = min_dis / 2
#     outFile = File("../data/filtered_points_" + str(min_dis) + ".las", mode="w", header=inFile.header)
#     indices_keep = []
#     flag = np.ones(len_input)
#     print("Minimum distance: ", min_dis)
#     for i in range(0, len_input):
#         if flag[i] == 0:
#             continue
#         p = Point3D(points[i, 0], points[i, 1], points[i, 2])
#         to_delete = myKdt.radius_query(p, min_dis)
#         # print(to_delete)
#         for j in range(len(to_delete)):
#             flag[to_delete[j]] = 0
#         # print(flag)
#         indices_keep.append(i)
#         print(i)
#
#     time_end = timeit.default_timer()
#     print('Processing time: ', time_end - time_start)
#     len_output = len(indices_keep)
#     print("output length: ", len_output)
#     ratio = (len_input - len_output)/len_input * 100
#     print("Reduction ratio: ", ratio, '%')
#     # header = "id, mini_dis, len_output, Reduction_rate, time"
#     line = str(l) + ',' + str(min_dis) + ',' + str(len_input) + ',' + \
#            str(len_output) + ',' + str(ratio) + ',' + str(time_end - time_start) + '\n'
#     stats.write(line)
#
#     points_keep = inFile.points[indices_keep]
#     outFile.points = points_keep
#     outFile.close()
#     if ratio < 50:
#         break
# stats.close()