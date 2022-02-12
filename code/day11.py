from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = data_dir / "test11.txt"
input_file = data_dir / "input11.txt"
with open(input_file, 'r') as f:
    m = [[int(c) for c in e.replace("\n", "")] for e in f.readlines()]


def get_neighbors(m, i, j):
    n = []
    shifts = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    for k, l in shifts:
        if 0 <= i+k < len(m) and 0 <= j+l < len(m[0]):
            n.append((i+k, j+l))
    return n


def review_cell(m, i, j, flashed):
    if m[i][j] > 9 and (i, j) not in flashed:
        flashed.append((i, j))
        # print("flash:", i, j)
        for n in get_neighbors(m, i, j):
            m[n[0]][n[1]] += 1
            review_cell(m, n[0], n[1], flashed)


def add_1(m):
    for i in range(len(m)):
        for j in range(len(m[0])):
            m[i][j] += 1


def nullify_flashed(m, flashed, total_count_l):
    for n in flashed:
        m[n[0]][n[1]] = 0
        total_count_l[0] += 1


def do_one_step(m, total_count_l):
    add_1(m)
    flashed = []
    for i in range(len(m)):
        for j in range(len(m[0])):
            review_cell(m, i, j, flashed)
    nullify_flashed(m, flashed, total_count_l)


# parts a and b
total_count_l = [0]
res_a, res_b = None, None
for i in range(1, 10000):  # should/could be a while loop
    do_one_step(m, total_count_l)
    if i == 100:
        res_a = total_count_l[0]
    if all([m[j][k] == 0 for k in range(len(m[0])) for j in range(len(m))]):
        res_b = i
        break

# display answers
print("answer a:", res_a)
print("answer b:", res_b)
