import copy
from collections import defaultdict
from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = data_dir / "test12.txt"
input_file = data_dir / "input12.txt"
with open(input_file, 'r') as f:
    inputs = [e.replace("\n", "").split("-") for e in f.readlines()]

map = defaultdict(list)
for c1, c2 in inputs:
    if c2 != "start":  # don't go back to start
        map[c1].append(c2)
    if c1 != "start":  # don't go back to start
        map[c2].append(c1)

# for display / debug, orders exploration alphabetically
for k, v in map.items():
    map[k] = sorted(v)


def explore1(cur_path, all_paths):
    if cur_path[-1] == "end":
        all_paths.append(cur_path)
        return
    for c in map[cur_path[-1]]:
        if c.isupper() or c not in cur_path:
            explore1(copy.deepcopy(cur_path) + [c], all_paths)


def explore2(cur_path_desc, all_paths):
    cur_path = cur_path_desc[0]
    allow_double = cur_path_desc[1]
    if cur_path[-1] == "end":
        all_paths.append(cur_path)
        return
    for c in map[cur_path[-1]]:
        if c.isupper() or c not in cur_path:
            explore2([copy.deepcopy(cur_path) + [c], allow_double], all_paths)
        elif allow_double and cur_path.count(c) == 1:
            explore2([copy.deepcopy(cur_path) + [c], False], all_paths)


# part a
all_paths_1 = []
explore1(["start"], all_paths_1)
res_a = len(all_paths_1)

# part b
all_paths_2 = []
explore2([["start"], True], all_paths_2)
res_b = len(all_paths_2)

# display answers
print("answer a:", res_a)
print("answer b:", res_b)
