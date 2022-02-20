from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = data_dir / "test13.txt"
input_file = data_dir / "input13.txt"
with open(input_file, 'r') as f:
    inputs = [e.replace("\n", "").split(",") for e in f.readlines()]

dots = [[int(e[0]), int(e[1])] for e in inputs if len(e) == 2]
folds = [e[0].split("=") for e in inputs if len(e) == 1 and e[0] != ""]
folds = [[e[0][-1], int(e[1])] for e in folds]


def fold(dots, fold):
    for d in dots:
        if fold[0] == "x":
            if d[0] > fold[1]:
                d[0] = 2 * fold[1] - d[0]
        if fold[0] == "y":
            if d[1] > fold[1]:
                d[1] = 2 * fold[1] - d[1]


res_a = None
for i in range(len(folds)):
    fold(dots, folds[i])
    if i == 0:
        res_a = len({(e[0], e[1]) for e in dots})

# display
final_dots = {(e[1], e[0]) for e in dots}
m, n = max([e[0] for e in final_dots]), max([e[1] for e in final_dots])
pic = []
for i in range(m+1):
    l = []
    for j in range(n+1):
        if (i, j) in final_dots:
            l.append("#")
        else:
            l.append(" ")
    pic.append("".join(l))

# answer a
print(res_a, "\n")

# answer b
for s in pic:
    print(s)
