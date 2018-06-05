import math

# Define parameters
KP = 5.0    # Attrctive potential gain
ETA = 100.0 # replusive potential gain



def cvt_coord_to_cube(index, dimension):
    res = []
    res.append(index // (dimension[0] * dimension[1]))
    index -= res[0] * dimension[0] * dimension[1]
    res.append(index // dimension[0])
    index -= res[1] * dimension[0]
    res.append(index)
    res.reverse()
    return res


def cal_attractive_potential(x, y, z, end_point, dimension):
    gx, gy, gz = cvt_coord_to_cube(end_point, dimension)
    return 0.5 * KP * math.sqrt((x - gx) ** 2 + (y - gy) ** 2 + (z - gz) ** 2)


def cal_replusive_potnetial():
    pass


def calculate_potential_field_map(nodes_list):
    for k in range(len(nodes_list[0][0])):
        for j in range(len(nodes_list[0])):
            for i in range(len(nodes_list)):
                pass

    return nodes_list


def potential_field_planning(nodes_list, dimension, boudnary, point_tree, start_index, end_index):
    # Define parameters
    c_dis = 5
    path = []
    potential_map = calculate_potential_field_map(nodes_list)

    return path


def main(nodes_list, dimension, boundary, start_end, point_tree):
    print("Start Potential Field Path Planning")
    # read start and end point
    start_index, end_index = start_end
    path = potential_field_planning(nodes_list, dimension, boundary, point_tree, start_index, end_index)





