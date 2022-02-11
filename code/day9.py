import math
from pyprojroot import here
data_dir = here("data")


# load input file
# input_file = data_dir / "test9.txt"
input_file = data_dir / "input9.txt"
with open(input_file, 'r') as f:
    m = [[int(c) for c in e.replace("\n", "")] for e in f.readlines()]


def is_lowest_neighboor(mat, l, c):
    nb_lines, nb_col = len(mat), len(mat[0])
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if mat[max(min(l+i, nb_lines-1), 0)][max(min(c+j, nb_col-1), 0)] < mat[l][c]:
            return False
    if mat[l][c] == 9:
        return False
    return True


# part a
nb_lines, nb_col = len(m), len(m[0])
res_a = 0
for i in range(nb_lines):
    for j in range(nb_col):
        if is_lowest_neighboor(m, i, j):
            res_a += 1 + m[i][j]

# part b
basins = []
for i in range(nb_lines):
    for j in range(nb_col):
        if m[i][j] == 9:
            continue
        ns = []
        if i > 0 and m[i-1][j] != 9: # same basin!
            ns.append((i-1, j))
        if j > 0 and m[i][j-1] != 9: # same basin!
            ns.append((i, j-1))
        matching_basins = [b for b in basins if any([n in b for n in ns])]
        if len(matching_basins) == 0:
            basins.append({(i, j)})
        elif len(matching_basins) == 1:
            [b for b in basins if any([n in b for n in ns])][0].add((i, j))
        else:
            basins = [bs for bs in basins if bs not in matching_basins]
            basins.append({(i, j)} | matching_basins[0] | matching_basins[1])
res_b = math.prod(sorted([len(b) for b in basins])[-3:])

# display answers
print("answer a:", res_a)
print("answer b:", res_b)