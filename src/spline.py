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


with open('../data/path.txt', 'r') as fp:
    path = fp.read().split(',')
del path[-1]
path = list(map(int, path))
print("path ", path)
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
tck, u = interpolate.splprep([x, y, z], s =2)
x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
print(x_knots, y_knots, z_knots)

fig2 = plt.figure(2)
ax3d = fig2.add_subplot(111, projection='3d')
ax3d.plot(x_knots, y_knots, z_knots, 'go')
ax3d.plot(x, y, z, 'b')
fig2.show()
plt.show()
