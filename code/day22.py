import collections
import math
from pyprojroot import here
data_dir = here("data")

# load input file
input_file = data_dir / "test22.txt"
# input_file = data_dir / "input22.txt"
with open(input_file, 'r') as f:
    raw_inputs = [e.replace("\n", "").split(",") for e in f.readlines()]

inputs = [[cuboide_desc[0][0:2], [[int(i) for i in e[1].split("..")] for e in [s.split("=") for s in cuboide_desc]]]
          for cuboide_desc in raw_inputs]


def deduce_range(cuboid, limits, add_1=False):
    if cuboid[0] > limits[1] or cuboid[1] < limits[0]:
        return 0, 0
    else:
        return max(limits[0], cuboid[0]), min(limits[1], cuboid[1]) + (1 if add_1 else 0)


limits = -50, 50
log = collections.defaultdict(bool)
for on_off, cuboide in inputs:
    x_range = deduce_range(cuboide[0], limits, add_1=True)
    y_range = deduce_range(cuboide[1], limits, add_1=True)
    z_range = deduce_range(cuboide[2], limits, add_1=True)
    for x in range(x_range[0], x_range[1]):
        for y in range(y_range[0], y_range[1]):
            for z in range(z_range[0], z_range[1]):
                log[(x, y, z)] = True if on_off == "on" else False

res_a = sum(log.values())

# arbitrary very low and very big numbers
min_value, max_value = -1000000, 1000000


def cuboide_add(cuboide1, cuboide2):
    dim_ranges = collections.defaultdict(list)
    for k in range(3):
        left_range = deduce_range(cuboide2[k], [min_value, cuboide1[k][0]])
        in_range = deduce_range(cuboide2[k], cuboide1[k])
        right_range = deduce_range(cuboide2[k], [cuboide1[k][1], max_value])
        # print(left_range, in_range, right_range)
        for r in [left_range, in_range, right_range]:
            if r != (0, 0):
                dim_ranges[k].append(r)
    return [cuboide1] + [(r1, r2, r3) for r1 in dim_ranges[0] for r2 in dim_ranges[1] for r3 in dim_ranges[2]]


def cuboide_remove(cuboide1, cuboide2):
    dim_ranges = collections.defaultdict(list)
    for k in range(3):
        left_range = deduce_range(cuboide1[k], [min_value, cuboide2[k][0]])
        in_range = deduce_range(cuboide1[k], cuboide2[k])
        right_range = deduce_range(cuboide1[k], [cuboide2[k][1], max_value])
        print(left_range, in_range, right_range)
        for i, r in enumerate([left_range, in_range, right_range]):
            if r != (0, 0):
                is_middle = i == 1
                dim_ranges[k].append([r, is_middle])
    return [(r1, r2, r3) for r1, is_mid1 in dim_ranges[0] for r2, is_mid2 in dim_ranges[1] for r3, is_mid3 in dim_ranges[2]
            if not is_mid1 or not is_mid2 or not is_mid3]


def cuboide_size(cuboide):
    return math.prod([r[1] - r[0] + 1 for r in cuboide])

# s = 0
# for on_off, cuboide in inputs[:1]:
#     s += cuboide_size(cuboide)
print(inputs)
cuboide1 = inputs[0][1]
cuboide2 = inputs[1][1]
print(sum([cuboide_size(e) for e in cuboide_remove(cuboide1, cuboide2)]))
print(cuboide_size(cuboide1))

cub1 = [[-3, 2], [-3, 2], [-3, 2]]
cub2 = [[-4, -3], [3, 4], [3, 4]]
diff12 = cuboide_remove(cub1, cub2)
print(sum([cuboide_size(c) for c in diff12]), diff12)
print(6*6*6)
# (_, cuboide1), (_, cuboide2) = inputs[0:2]
# print([cuboide1, cuboide2])
# # print(cuboide_add(cuboide1, cuboide2))
# cr = cuboide_remove(cuboide1, cuboide2)
# print(len(cr), cr)
#
#
# print(cuboide_size([[0, 1], [0, 1], [0, 2]]))



# display answers
print("answer a:", res_a)
# print("answer b:", res_b)
