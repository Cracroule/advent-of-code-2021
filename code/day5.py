from pyprojroot import here
data_dir = here("data")

# load input file
# file = open('test5a.txt', 'r')
file = open(data_dir / 'input5.txt', 'r')
all_inputs = [e.replace('\n', '').split(" -> ") for e in file.readlines()]
inputs = [[[int(e) for e in r[0].split(",")],
           [int(e) for e in r[1].split(",")]] for r in all_inputs]
max_x = max([max(r[0][0], r[1][0]) for r in inputs])
max_y = max([max(r[0][1], r[1][1]) for r in inputs])

# part a
m = list()  # create matrix
for y in range(max_y + 1):
    m.append([0] * (max_x + 1))

for w in inputs:
    if w[0][0] == w[1][0]:
        x = w[0][0]
        y1 = w[0][1]
        y2 = w[1][1]
        for y_i, _ in enumerate(m):
            if min(y1, y2) <= y_i <= max(y1, y2):
                m[y_i][x] += 1
    if w[0][1] == w[1][1]:
        y = w[0][1]
        x1 = w[0][0]
        x2 = w[1][0]
        for x_i, _ in enumerate(m[y]):
            if min(x1, x2) <= x_i <= max(x1, x2):
                m[y][x_i] += 1

res_a = sum([e >= 2 for r in m for e in r])

# part b
m = list()  # create matrix
for y in range(max_y + 1):
    m.append([0] * (max_x + 1))

for w in inputs:
    if w[0][0] == w[1][0]:
        x = w[0][0]
        y1 = w[0][1]
        y2 = w[1][1]
        for y_i, _ in enumerate(m):
            if min(y1, y2) <= y_i <= max(y1, y2):
                m[y_i][x] += 1
    if w[0][1] == w[1][1]:
        y = w[0][1]
        x1 = w[0][0]
        x2 = w[1][0]
        for x_i, _ in enumerate(m[y]):
            if min(x1, x2) <= x_i <= max(x1, x2):
                m[y][x_i] += 1
    if abs(w[1][0] - w[0][0]) == abs(w[1][1] - w[0][1]):
        n = abs(w[1][0] - w[0][0]) + 1
        x_s = w[0][0]
        y_s = w[0][1]
        x_dir = (w[1][0] - w[0][0]) / abs(w[1][0] - w[0][0])
        y_dir = (w[1][1] - w[0][1]) / abs(w[1][1] - w[0][1])
        for i in range(n):
            m[y_s + int(i * y_dir)][x_s + int(i * x_dir)] += 1

res_b = sum([e >= 2 for r in m for e in r])

# display results
print("answer a:", res_a)
print("answer b:", res_b)
