from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = data_dir / "test20.txt"
input_file = data_dir / "input20.txt"
with open(input_file, 'r') as f:
    raw_inputs = [l.replace("\n", "") for l in f.readlines()]

compr_rules = raw_inputs[0]
image = raw_inputs[2:]


def pad_image(input_image, pad_value=".", n=1):
    if n == 0:
        return input_image
    new_image = [pad_value * (len(input_image[0]) + 2)]
    for l in input_image:
        new_image.append(pad_value + l + pad_value)
    new_image.append(pad_value * (len(input_image[0]) + 2))
    return pad_image(new_image, pad_value, n-1)


def get_pixel_score(m, i, j, missing_val="."):
    n = []
    shifts = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
    for k, l in shifts:
        if 0 <= i+k < len(m) and 0 <= j+l < len(m[0]):
            if m[i+k][j+l] == "#":
                n.append("1")
            else:
                n.append("0")
        else:
            n.append("1" if missing_val == "#" else "0")
    return int("".join(n), 2)


def convert_pixel(m, i, j, compr_rules, missing_val="."):
    return compr_rules[get_pixel_score(m, i, j, missing_val)]


def convert_pixel_debug(m, i, j, compr_rules, missing_val="."):
    return " " + str(get_pixel_score(m, i, j, missing_val)) + " "


def convert_image(image, compr_rules, missing_val=".", debug=False):
    image = pad_image(image, missing_val, 1)
    converted_image = []
    for i in range(len(image)):
        tmp = []
        for j in range(len(image[0])):
            # if not debug:
            tmp.append(convert_pixel(image, i, j, compr_rules, missing_val))
            # else:
            #     tmp.append(convert_pixel_debug(image, i, j, compr_rules, missing_val))
        converted_image.append("".join(tmp))
    return converted_image


def print_image(input_image):
    for row in input_image:
        print(row)


for i in range(2):
    image = convert_image(image, compr_rules, missing_val="." if i % 2 == 0 else "#")
res_a = "".join([*image]).count("#")

for i in range(2, 50):
    image = convert_image(image, compr_rules, missing_val="." if i % 2 == 0 else "#")
res_b = "".join([*image]).count("#")


# display answers
print("answer a:", res_a)
print("answer b:", res_b)
