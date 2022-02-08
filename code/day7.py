import statistics
from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = "test7.txt"
input_file = data_dir / "input7.txt"
with open(input_file, 'r') as f:
    all_inputs = [e.replace("\n", "").split(",") for e in f.readlines()]
inputs = [int(i) for i in all_inputs[0]]

# part a
x_obj = int(statistics.median(inputs))
res_a = sum([abs(i - x_obj) for i in inputs])


# part b
def cost(dist):
    return int(dist * (dist + 1) / 2)


res_b = min([sum([cost(abs(i - x_obj)) for i in inputs]) for x_obj in range(1, max(inputs) + 1)])

# display results
print("answer a:", res_a)
print("answer b:", res_b)
