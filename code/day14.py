from collections import defaultdict
from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = data_dir / "test14.txt"
input_file = data_dir / "input14.txt"
with open(input_file, 'r') as f:
    inputs = [e.replace("\n", "") for e in f.readlines()]
    # m = [[int(c) for c in e.replace("\n", "")] for e in f.readlines()]

polym = [c for c in inputs[0]]
rules = [c.split(" -> ") for c in inputs[2:]]
rules = {e[0]: e[1] for e in rules}

# naive part a
# def perform_step(polym, rules):
#     to_insert = []
#     for i in range(1, len(polym)):
#         cur_pair = polym[i-1] + polym[i]
#         if cur_pair in rules.keys():
#             to_insert.append((i, rules[cur_pair]))
#
#     # actually insert them all
#     counter = 0
#     for pos, c in to_insert:
#         polym.insert(pos + counter, c)
#         counter += 1


# less naive to comply with part b (naive way too computationally expensive!)
def perform_step_compressed(cpolym, rules):
    cpolym_new = defaultdict(int)
    for k, v in cpolym.items():
        cpolym_new[k[0] + rules[k]] += v
        cpolym_new[rules[k] + k[1]] += v
    return cpolym_new


def convert_compressed_to_table(cpolym, polym_start, polym_end):
    c_table = defaultdict(int)
    c_table[polym_start], c_table[polym_end] = 1, 1  # these letters appear in 1 pair instead of 2
    for k, v in cpolym.items():
        c_table[k[0]] += v
        c_table[k[1]] += v
    return sorted([(int(v/2), k) for k, v in c_table.items()])


polym_start, polym_end = polym[0], polym[-1]
cpolym = defaultdict(int)
for i in range(1, len(polym)):
    cpolym[polym[i-1] + polym[i]] += 1

res_a, res_b = None, None
for i in range(40):
    cpolym = perform_step_compressed(cpolym, rules)
    if i + 1 == 10:
        polym_table = convert_compressed_to_table(cpolym, polym_start, polym_end)
        res_a = polym_table[-1][0] - polym_table[0][0]
polym_table = convert_compressed_to_table(cpolym, polym_start, polym_end)
res_b = polym_table[-1][0] - polym_table[0][0]

# display answers
print("answer a:", res_a)
print("answer b:", res_b)
