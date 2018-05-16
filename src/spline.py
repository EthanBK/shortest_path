

def cvt_coord_to_cube(index):
    res = []
    res.append(index // (dimension[0] * dimension[1]))
    index -= res[0] * dimension[0] * dimension[1]
    res.append(index // dimension[0])
    index -= res[1] * dimension[0]
    res.append(index)
    res.reverse()
    return res


def cvt_coord_to_line(index_list):
    res = index_list[0]
    res += index_list[1] * dimension[0]
    res += index_list[2] * dimension[0] * dimension[1]
    return res


with open('../data/path.txt', 'r') as fp:
    path = fp.read().split(',')
del path[-1]
path = list(map(int, path))
print("path ", path)
with open('../data/dimension.txt', 'r') as fp:
    dimension = fp.read().split(',')
del dimension[-1]
dimension = list(map(int, path))
print("dimension ", dimension)

print(cvt_coord_to_line([22, 33, 1]))
print(cvt_coord_to_cube(2516974))
