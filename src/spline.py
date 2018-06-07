import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D


def cvt_coord_to_line(index_list, dimension):
    res = index_list[0]
    res += index_list[1] * dimension[0]
    res += index_list[2] * dimension[0] * dimension[1]
    return res


def cvt_coord_to_cube(index):
    res = []
    res.append(index // (dimension[0] * dimension[1]))
    index -= res[0] * dimension[0] * dimension[1]
    res.append(index // dimension[0])
    index -= res[1] * dimension[0]
    res.append(index)
    res.reverse()
    return res


fig2 = plt.figure(2)
ax3d = fig2.add_subplot(111, projection='3d')

# Load Dijkstra's path
with open('../data/path_dpp.txt', 'r') as fp:
    path = fp.read().split(',')
del path[-1]
path = list(map(int, path))
print("path ", path)

# Load dimension data
with open('../data/dimension.txt', 'r') as fp:
    dimension = fp.read().split(',')
del dimension[-1]
dimension = list(map(int, dimension))
print("dimension ", dimension)

#  convert index to xyz coordinate
x, y, z = [], [], []
for item in path:
    coord = cvt_coord_to_cube(item)
    x.append(coord[0])
    y.append(coord[1])
    z.append(coord[2])

# spline interpolation
num_sample_pts = 100
tck, u = interpolate.splprep([x, y, z], s=2)
x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
u_sample = np.linspace(0, 1, num_sample_pts)
x_sp, y_sp, z_sp = interpolate.splev(u_sample, tck)

ax3d.plot(x_knots, y_knots, z_knots, 'go', label='knots(dpp)')
ax3d.plot(x_sp, y_sp, z_sp, 'g', label='B-spline(dpp)')
ax3d.plot(x, y, z, 'b', label='true(dpp)')


# PFPP

# Load Dijkstra's path
with open('../data/path_pfpp.txt', 'r') as fp:
    path = fp.read().split(',')
del path[-1]
path = list(map(int, path))
print("path ", path)

#  convert index to xyz coordinate
x, y, z = [], [], []
for item in path:
    coord = cvt_coord_to_cube(item)
    x.append(coord[0])
    y.append(coord[1])
    z.append(coord[2])

# spline interpolation
num_sample_pts = 100
tck, u = interpolate.splprep([x, y, z], s=2)
x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
u_sample = np.linspace(0, 1, num_sample_pts)
x_sp, y_sp, z_sp = interpolate.splev(u_sample, tck)


ax3d.plot(x_knots, y_knots, z_knots, 'ro', label='knots(pfpp)')
ax3d.plot(x_sp, y_sp, z_sp, 'r', label='B-spline(pfpp)')
ax3d.plot(x, y, z, 'y', label='true(pfpp)')
ax3d.legend()
fig2.show()
plt.show()
fig2.savefig('../data/spline.png')
