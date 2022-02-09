from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = data_dir / "test8.txt"
input_file = data_dir / "input8.txt"
with open(input_file, 'r') as f:
    all_inputs = [e.replace("\n", "").split(" | ") for e in f.readlines()]
inputs = [[r[0].split(" "), r[1].split(" ")] for r in all_inputs]

# part a
counter = 0
for r in inputs:
    counter += len([e for e in r[1] if len(e) in (2, 3, 4, 7)])
res_a = counter

counter = 0
for r in inputs:
    # print("inputs:", ["".join(sorted([e for e in s])) for s in r[0]])
    # print("outputs:", ["".join(sorted([e for e in s])) for s in r[1]])
    d = {k: set([w for w in r[0] if len(w) == v][0]) for k, v in {1: 2, 7: 3, 4: 4, 8: 7}.items()}
    w_6l, w_5l = [w for w in r[0] if len(w) == 6], [w for w in r[0] if len(w) == 5]
    missing_l_w_6l, missing_l_w_5l = [list(d[8] - set(w))[0] for w in w_6l], [list(d[8] - set(w)) for w in w_5l]
    p3_l = list(d[1].intersection(missing_l_w_6l))[0]
    p6_l = list(d[1] - set(p3_l))[0]
    d[2] = d[8] - set([w for w in missing_l_w_5l if p6_l in w][0])
    missing_l_for_five = set([w for w in missing_l_w_5l if p3_l in w][0])
    p5_l = list(missing_l_for_five - set(p3_l))[0]
    d[5] = d[8] - missing_l_for_five
    d[3] = d[8] - set([w for w in missing_l_w_5l if (p6_l not in w and p3_l not in w)][0])
    d[6], d[9] = d[8] - set(p3_l), d[8] - set(p5_l)
    d[0] = [set(w) for w in w_6l if set(w) != d[6] and set(w) != d[9]][0]

    counter += int("".join([str([d[i] for i in range(10)].index(e)) for e in [set(e) for e in r[1]]]))

    # debug
    # print("encoding:", ["".join(sorted(e)) for e in [d[i] for i in range(10)]])
    # output = "".join([str([d[i] for i in range(10)].index(e)) for e in [set(e) for e in r[1]]])
    # print("res:", output)

res_b = counter

# display results
print("answer a:", res_a)
print("answer b:", res_b)
