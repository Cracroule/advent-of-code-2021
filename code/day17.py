import math
from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = data_dir / "test17.txt"
input_file = data_dir / "input17.txt"
with open(input_file, 'r') as f:
    inputs = [e.replace("\n", "").replace(",", "").split(" ") for e in f.readlines()]
inputs = [e[2:].split("..") for e in inputs[0][2:]]
(xt_min, xt_max), (yt_min, yt_max) = [(int(e[0]), int(e[1])) for e in inputs]
print((xt_min, xt_max), (yt_min, yt_max))


def is_square(k):
    return k == int(math.sqrt(k) + 0.5) ** 2


s = set()
n_max = - 2 * yt_min + 1  # only works if yt_min is negative though...
for n in range(1, n_max+1):
    s_x, s_y = [], []
    for x in range(xt_min, xt_max+1):
        if (2 * x + n * (n-1)) % (2 * n) == 0:
            vx = (2 * x + n * (n - 1)) // (2 * n)
            if n <= vx:
                s_x.append(vx)
        if is_square(1 + 8 * x) and int(math.sqrt(1 + 8 * x) - 1) % 2 == 0:
            vx = (int(math.sqrt(1 + 8 * x)) - 1) // 2
            if n > vx:
                s_x.append(vx)
    for y in range(yt_min, yt_max+1):
        if (2 * y + n * (n-1)) % (2 * n) == 0:
            s_y.append((2 * y + n * (n - 1)) // (2 * n))
    # print(s_x, s_y)
    for vx in s_x:
        for vy in s_y:
            s.add((vx, vy))

res_a = int((- yt_min) * (-yt_min -1)) // 2  # only works if yt_min is negative though...
res_b = len(s)

# display answers
print("answer a:", res_a)
print("answer b:", res_b)

# # visual debug below
# vx, vy = 6, 8
# def get_x(vx_init, n):
#     if n > vx_init:
#         return int(vx_init * (vx_init+1)/2)
#     else:
#         return int(n * vx_init - n * (n - 1) / 2)
#
# def get_y(vy_init, n):
#     nn = n * (n - 1) / 2
#     return int(n * vy_init - nn)

# for i in range(30):
#     print(i, "-->", get_x(vx, i), get_y(vy, i))

