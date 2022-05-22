from pyprojroot import here
data_dir = here("data")


def find_deepest_level(inputs):
    level, max_level = 0, 0
    for i in range(len(inputs)):
        if inputs[i] == "[":
            level += 1
        if inputs[i] == "]":
            level -= 1
        max_level = max(level, max_level)
    return max_level


def find_pair_indices(inputs, target_level):
    level, max_level, indices = 0, 0, []
    for i in range(len(inputs)):
        if inputs[i] == "[":
            level += 1
        if level == target_level:
            indices.append(i)
        if inputs[i] == "]":
            level -= 1
        if len(indices) and level != target_level:
            return indices


def get_pair_values(inputs, pair_indices):
    pair_str = "".join([inputs[i] for i in pair_indices])
    v1, v2 = [int(e) for e in pair_str.replace("[", "").replace("]", "").split(",")]
    return v1, v2


def find_near_value_indices(inputs, start, direction):
    i, indices = start, []
    while 0 <= i < len(inputs):
        if inputs[i] not in ("[", ',', "]"):
            indices.append(i)
        elif len(indices):
            return sorted(indices)
        i += direction
    return sorted(indices) if len(indices) else None


def find_to_be_split_indices(inputs):
    i, indices = 0, []
    while 0 <= i < len(inputs):
        if inputs[i] not in ("[", ',', "]"):
            indices.append(i)
        elif len(indices):
            v = int(get(inputs, sorted(indices)))
            if v > 9:
                return sorted(indices)
            else:
                indices = []
        i += 1
    if len(indices):
        v = int(get(inputs, sorted(indices)))
        if v > 9:
            return sorted(indices)
    return None


def inject_value(inputs, value, indices):
    return inputs[:min(indices)] + str(value) + inputs[(max(indices) + 1):], len(value) - len(indices)


def get(inputs, indices):
    return "".join([inputs[i] for i in indices]) if indices is not None else None


def reduce(inputs):
    while True:
        max_lvl = find_deepest_level(inputs)
        if max_lvl > 4:  # explode!
            explode_indices = find_pair_indices(inputs, max_lvl)
            v1, v2 = get_pair_values(inputs, explode_indices)
            left_v_i = find_near_value_indices(inputs, min(explode_indices) - 1, -1)
            right_v_i = find_near_value_indices(inputs, max(explode_indices) + 1, 1)
            shift1, shift2 = 0, 0
            if left_v_i is not None:
                inputs, shift1 = inject_value(inputs, str(v1 + int(get(inputs, left_v_i))), left_v_i)
            inputs, shift2 = inject_value(inputs, "0", [e + shift1 for e in explode_indices])
            if right_v_i is not None:
                right_v_i = [e + shift1 + shift2 for e in right_v_i]
                inputs, _ = inject_value(inputs, str(v2 + int(get(inputs, right_v_i))), right_v_i)
            continue  # explosion done, we restart

        to_split_indices = find_to_be_split_indices(inputs)
        if to_split_indices is not None:  # split !
            v = int(get(inputs, to_split_indices))
            repl_v = "[" + str(v // 2) + "," + str(v // 2 + v % 2) + "]"
            inputs, _ = inject_value(inputs, repl_v, to_split_indices)
            continue  # split done, we restart
        break
    return inputs


def get_magnitude(inputs):
    inputs_m, magn = str(inputs), None  # make a copy
    while "," in inputs_m:
        indices_deepest_pair = find_pair_indices(inputs_m, find_deepest_level(inputs_m))
        v1, v2 = get_pair_values(inputs_m, indices_deepest_pair)
        magn = v1 * 3 + v2 * 2
        inputs_m, _ = inject_value(inputs_m, str(magn), indices_deepest_pair)
    return int(magn)


# # load input file
# input_file = data_dir / "test18.txt"
input_file = data_dir / "input18.txt"
with open(input_file, 'r') as f:
    raw_inputs = [e.replace("\n", "") for e in f.readlines()]

inputs = raw_inputs[0]
for i in range(1, len(raw_inputs)):
    inputs = reduce("[" + inputs + "," + raw_inputs[i] + "]")

res_a = get_magnitude(inputs)

res_b = 0
for i in range(len(raw_inputs)):
    for j in range(len(raw_inputs)):
        if i != j:
            res_b = max(res_b, get_magnitude(reduce("[" + raw_inputs[i] + "," + raw_inputs[j] + "]")))

# display answers
print("answer a:", res_a)
print("answer b:", res_b)
