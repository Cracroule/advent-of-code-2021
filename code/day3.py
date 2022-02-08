import copy
from pyprojroot import here
data_dir = here("data")


def get_col(i, l):
    return [e[i] for e in l]


def most_common(l):
    # returns 1 if ties (oxygen rule, day 3)
    if l.count(0) <= l.count(1):
        return 1
    return 0


def convert_to_int(base_2_lst):
    return int("".join([str(i) for i in base_2_lst]), 2)


# load input file
# file = open('test3a.txt', 'r')
file = open(data_dir / 'input3.txt', 'r')
l = [[int(b) for b in e.replace('\n', '')] for e in file.readlines()]
n_col = len(l[0])

# part a
gamma, epsilon = list(), list()
for i in range(n_col):
    gamma.append(most_common(get_col(i, l)))
    epsilon.append(1 - gamma[-1])

res_a = convert_to_int(gamma) * convert_to_int(epsilon)

# part b
l_ox, l_co2 = copy.deepcopy(l), copy.deepcopy(l)
ox, co2 = None, None
for i in range(len(l_ox[0])):
    if ox is None:
        mc_ox = most_common(get_col(i, l_ox))
        l_ox = [r for r in l_ox if r[i] == mc_ox]
        if len(l_ox) == 1:
            ox = convert_to_int(l_ox[0])
    if co2 is None:
        mc_co2 = most_common(get_col(i, l_co2))
        l_co2 = [r for r in l_co2 if r[i] == (1-mc_co2)]
        if len(l_co2) == 1:
            co2 = convert_to_int(l_co2[0])
            # break
    if ox is not None and co2 is not None:
        break

res_b = ox * co2

# display results
print("answer a:", res_a)
print("answer b:", res_b)
