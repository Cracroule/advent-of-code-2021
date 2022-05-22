from copy import deepcopy
from collections import defaultdict
from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = data_dir / "test19.txt"
input_file = data_dir / "input19.txt"
with open(input_file, 'r') as f:
    raw_inputs = [e.replace("\n", "") for e in f.readlines()]

all_scanners = []
cur_scanner = []
for l in raw_inputs:
    if l[0:2] == "--":
        cur_scanner = []
    elif l == "":
        all_scanners.append(cur_scanner)
    else:
        cur_scanner.append(tuple([int(e) for e in l.split(",")]))
all_scanners.append(cur_scanner)
nb_scanners = len(all_scanners)


def dist(p1, p2):
    return sum([(p1[k] - p2[k]) ** 2 for k in range(3)])


def diff(p1, p2):
    return tuple([p1[k] - p2[k] for k in range(3)])


def add_points(p1, p2):
    return tuple([p1[k] + p2[k] for k in range(3)])


def change_referential(point, rotation, translation):
    return add_points([rotation[i][1] * point[rotation[i][0]] for i in range(3)], translation)


m_distances = []
for scanner in all_scanners:
    all_dist_scanner = []
    for i, bi in enumerate(scanner):
        all_dist_i = []
        for j, bj in enumerate(scanner):
            all_dist_i.append(dist(bi, bj))
        all_dist_scanner.append(all_dist_i)
    m_distances.append(all_dist_scanner)

# print("nb scanners:", nb_scanners)

# IDENTIFY PAIRS OF SCANNERS USING DISTANCE PATTERNS
scanner_pairs = []
matching_beacons_indices = defaultdict(set)
for s1, s2 in [(s1, s2) for s1 in range(nb_scanners) for s2 in range(nb_scanners) if s1 < s2]:
    common_distances = []
    for i, b_i in enumerate(m_distances[s1]):
        common_distances_i = []
        for j, b_j in enumerate(m_distances[s2]):
            common_distances_i.append(sum([d in b_j for d in b_i]))
        common_distances.append(common_distances_i)
    for i, cd_i in enumerate(common_distances):
        for j, n in enumerate(cd_i):
            if n >= 12:
                matching_beacons_indices[(s1, s2)].add((i, j))

    if len(matching_beacons_indices[(s1, s2)]) >= 12:
        scanner_pairs.append((s1, s2))

# print(len(matching_beacons_indices), len(set(matching_beacons_indices)))
# print(len(scanner_pairs), scanner_pairs)

ordered_scanner_pairs, scanner_pairs = [], set(scanner_pairs)
priority_ind = {0}
while len(priority_ind) != nb_scanners:
    temporart_priority_ind = set()
    for s1, s2 in scanner_pairs:
        if s1 in priority_ind and s2 not in priority_ind and s2 not in temporart_priority_ind:
            temporart_priority_ind.add(s2)
            ordered_scanner_pairs.append((s1, s2))
        if s2 in priority_ind and s1 not in priority_ind and s1 not in temporart_priority_ind:
            temporart_priority_ind.add(s1)
            ordered_scanner_pairs.append((s2, s1))
    priority_ind.update(temporart_priority_ind)

# print(len(ordered_scanner_pairs), ordered_scanner_pairs)

# FIND ROTATIONS AND TRANSLATIONS FOR EACH PAIR OF SCANNERS SHARING 12 POINTS
rotations = defaultdict(dict)
translations = dict()
final_points = deepcopy(all_scanners)
scanners_coords = {i: [(0, 0, 0)] for i in range(nb_scanners)}
for s1, s2 in ordered_scanner_pairs[::-1]:
    s1s2_key = tuple(sorted([s1, s2]))
    s1_i = [e[0 if s1 < s2 else 1] for e in matching_beacons_indices[tuple(sorted([s1, s2]))]]
    s2_i = [e[1 if s1 < s2 else 0] for e in matching_beacons_indices[tuple(sorted([s1, s2]))]]

    i_ref = 0  # arbitrary reference point
    s1_v = [diff(all_scanners[s1][s1_i[i_ref]], all_scanners[s1][i]) for i in s1_i]
    s2_v = [diff(all_scanners[s2][s2_i[i_ref]], all_scanners[s2][i]) for i in s2_i]

    for i in range(3):  # use relative vectors within referential to deduce rotation pattern
        s1_dim_i = tuple(e[i] for e in s1_v)
        for j in range(3):
            for sign in (1, -1):
                if s1_dim_i == tuple(sign * e[j] for e in s2_v):
                    rotations[(s1, s2)][i] = (j, sign)
    assert(len(rotations[(s1, s2)].keys()) == 3)  # check we found our 3 dimensions

    k, b_i = 0, s2_i[0]  # deduce the origin using a single point (say the first one)
    p2_rotated = [rotations[(s1, s2)][i][1] * all_scanners[s2][b_i][rotations[(s1, s2)][i][0]] for i in range(3)]
    p1_coord = all_scanners[s1][s1_i[k]]
    translations[(s1, s2)] = diff(p1_coord, p2_rotated)
    assert(tuple(all_scanners[s1][s1_i[k]]) == tuple(
        change_referential(all_scanners[s2][b_i], rotations[(s1, s2)], translations[(s1, s2)])))

    scanners_coords[s1].extend([change_referential(p, rotations[(s1, s2)], translations[(s1, s2)])
                                for p in scanners_coords[s2]])
    final_points[s1] = final_points[s1] + [change_referential(final_points[s2][i], rotations[(s1, s2)],
                                                              translations[(s1, s2)])
                                           for i in range(len(final_points[s2]))]

# solve a
all_final_points = set(final_points[0])
res_a = len(all_final_points)

# solve b
res_b = 0
all_scanners_coords = scanners_coords[0]
for i in range(len(all_scanners_coords)):
    for j in range(i + 1, len(all_scanners_coords)):
        res_b = max(res_b, sum([abs(all_scanners_coords[i][k] - all_scanners_coords[j][k]) for k in range(3)]))

# display answers
print("answer a:", res_a)
print("answer b:", res_b)
