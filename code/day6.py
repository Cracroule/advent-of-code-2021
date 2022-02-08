from collections import defaultdict
from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = "test6.txt"
input_file = "input6.txt"
with open(data_dir / input_file, 'r') as f:
    all_inputs = [e.replace("\n", "").split(",") for e in f.readlines()]
inputs = [int(i) for i in all_inputs[0]]

# both parts below
d = defaultdict(int)
for i in inputs:
    d[i] += 1

for day in range(1, 256+1):
    dn = defaultdict(int)
    dn[8] += d[0]
    dn[6] += d[0]
    for i in range(8):
        dn[i] += d[i+1]
    d = dn
    if day == 80:
        print("part a:", sum(dn.values()))

print("part b:", sum(dn.values()))

# # display results
# print("answer a:", res_a)
# print("answer b:", res_b)
