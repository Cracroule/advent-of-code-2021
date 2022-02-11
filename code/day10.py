import statistics
from pyprojroot import here
data_dir = here("data")


# load input file
# input_file = data_dir / "test10.txt"
input_file = data_dir / "input10.txt"
with open(input_file, 'r') as f:
    inputs = [[c for c in e.replace("\n", "")] for e in f.readlines()]

# part a
d = {"{": "}", "(": ")", "[": "]", "<": ">"}
reversed_d = {v: k for k, v in d.items()}
scoring_d = {"}": 1197, ")": 3, "]": 57, ">": 25137}
res_a = 0
for l in inputs:
    cur_seq = []
    for c in l:
        if c in d.keys():
            cur_seq.append(c)
        else:
            if cur_seq[-1] == reversed_d[c]:
                cur_seq = cur_seq[:-1]
            else:
                res_a += scoring_d[c]
                break

# part b
d = {"{": "}", "(": ")", "[": "]", "<": ">"}
reversed_d = {v: k for k, v in d.items()}
scoring_d = {"}": 3, ")": 1, "]": 2, ">": 4}
all_scores = []
for l in inputs:
    cur_seq = []
    for i in range(len(l)):
        c = l[i]
        if c in d.keys():
            cur_seq.append(c)
        else:
            if cur_seq[-1] == reversed_d[c]:
                cur_seq = cur_seq[:-1]
            else:
                break
        if i == len(l) - 1:  # incomplete line!
            missing = [d[e] for e in cur_seq[::-1]]
            l_score = 0
            for m in missing:
                l_score *= 5
                l_score += scoring_d[m]
            all_scores.append(l_score)
res_b = statistics.median(all_scores)

# display answers
print("answer a:", res_a)
print("answer b:", res_b)