from pyprojroot import here
data_dir = here("data")

# load input file
# file = open('test2a.txt', 'r')
file = open(data_dir / 'input2.txt', 'r')
l = [e.replace('\n', '').split(" ") for e in file.readlines()]

# part a
p = [0, 0]
for instr in l:
    mv = int(instr[1])
    if instr[0] == "forward":
        p[0] += mv
    elif instr[0] == "down":
        p[1] += mv
    elif instr[0] == "up":
        p[1] -= mv
    else:
        Exception("unknown instruction")
res_a = p[0] * p[1]

# part b
p = [0, 0]
aim = 0
for instr in l:
    mv = int(instr[1])
    if instr[0] == "forward":
        p[0] += mv
        p[1] += aim * mv
    elif instr[0] == "down":
        aim += mv
    elif instr[0] == "up":
        aim -= mv
    else:
        Exception("unknown instruction")
    # print(p, aim)
res_b = p[0] * p[1]

# display results
print("answer a:", res_a)
print("answer b:", res_b)
