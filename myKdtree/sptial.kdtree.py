import numpy as np
import scipy.spatial as spatial
from laspy.file import File
import timeit
import itertools

# Minimum distance
min_dis = 1

stats = open('../data/stats.csv', 'w')
header = "id,mini_dis,len_input,len_output,Reduction_rate,time" + '\n'
stats.write(header)

# .las file read and write
inFile = File('fn.las', mode='r')
# Pre-load .las into numpy array
points = np.transpose(np.array([inFile.x, inFile.y, inFile.z]))
# len_input = points.shape[0]
len_input = points.shape[0]
# insert points into kd-tree
t1 = timeit.default_timer()
point_tree = spatial.cKDTree(points[:len_input])
t2 = timeit.default_timer()
line = "-1,Insertion,,,," + str(t2 - t1) + '\n'
stats.write(line)
print("Insertion Complete.")

for l in itertools.count():
    time_start = timeit.default_timer()
    min_dis = min_dis / 2
    outFile = File("../data/filtered_points_" + str(min_dis) + ".las", mode="w", header=inFile.header)
    indices_keep = []

    flag = np.ones(len_input)
    print("Minimum distance: ", min_dis)
    for i in range(0, len_input):
        if flag[i] == 0:
            continue
        to_delete = point_tree.query_ball_point(points[i], min_dis)
        # print(to_delete)
        for j in range(len(to_delete)):
            flag[to_delete[j]] = 0
        # print(flag)
        indices_keep.append(i)
        print(i)

    time_end = timeit.default_timer()
    print('Processing time: ', time_end - time_start)
    len_output = len(indices_keep)
    print("output length: ", len_output)
    ratio = (len_input - len_output)/len_input * 100
    print("Reduction ratio: ", ratio, '%')
    # header = "id, mini_dis, len_output, Reduction_rate, time"
    line = str(l) + ',' + str(min_dis) + ',' + str(len_input) + ',' + \
           str(len_output) + ',' + str(ratio) + ',' + str(time_end - time_start) + '\n'
    stats.write(line)

    points_keep = inFile.points[indices_keep]
    outFile.points = points_keep
    outFile.close()
    if ratio < 50:
        break
stats.close()