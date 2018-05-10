from Point3D import Point3D
from KdTree import KdTree
from KdTree_noCube import KdTree as KdTree_nc
import scipy.spatial as spatial
import numpy as np
import timeit
from laspy.file import File
import itertools
import random

min_dis = 1

stats = open('../data/test_insert.csv', 'a')
header = "id,num_insert,spatial time, myKdTree time" + '\n'
stats.write(header)

# len_input = points.shape[0]
len_input_start = 100000
len_input_end = 10000000
max_value = 2000000
# insert points into kd-tree


for t in itertools.count():
    len = len_input_start * t
    points = np.random.rand(3, len)
    t0 = timeit.default_timer()
    point_tree = spatial.KDTree(points)
    t1 = timeit.default_timer()

    t2 = timeit.default_timer()
    # myKdt = KdTree()
    mykdtnc = KdTree_nc()
    for i in range(len):
        p = Point3D(points[0, i], points[1, i], points[2, i])
        #myKdt.insert(i, p)
        mykdtnc.insert(i, p)
    t3 = timeit.default_timer()

    stats = open('../data/test_insert.csv', 'a')
    line = str(t) + ',' + str(len) + ',' + str(t1 - t0) + ',' + str(t3 - t2) + '\n'
    stats.write(line)
    print("Insertion Complete. Time: sp ", t2 - t1, ". my ", t3 - t2)

stats.close()
