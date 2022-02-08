from pyprojroot import here
data_dir = here("data")

# part a
file = open(data_dir / 'input1.txt', 'r')
l = [int(e.replace('\n', '')) for e in file.readlines()]
res_a = sum([l[i+1] > l[i] for i in range(len(l) - 1)])

# part b
file = open(data_dir / 'input1.txt', 'r')
l = [int(e.replace('\n', '')) for e in file.readlines()]
l2 = [sum(l[i:i+3]) for i in range(len(l) - 2)]
res_b = sum([l2[i+1] > l2[i] for i in range(len(l2) - 1)])

# display answers
print("answer a:", res_a)
print("answer b:", res_b)
