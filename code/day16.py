import math
from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = data_dir / "test16.txt"
input_file = data_dir / "input16.txt"

with open(input_file, 'r') as f:
    hex_input = f.readlines()[0].replace("\n", "")

# hex_input = "D2FE28"
# hex_input = "38006F45291200"
# hex_input = "EE00D40C823060"
# hex_input = "8A004A801A8002F478"
# hex_input = "620080001611562C8802118E34"
# hex_input = "C0015000016115A2E0802F182340"
# hex_input = "A0016C880162017C3686B18A3D4780"
# hex_input = "9C0141080250320F1802104A08"
hex_d = {"0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101", "6": "0110",
         "7": "0111", "8": "1000", "9": "1001", "A": "1010", "B": "1011", "C": "1100", "D": "1101",
         "E": "1110", "F": "1111"}
bin_input = "".join([hex_d[c] for c in hex_input])


def perform_operation(type_id, values):
    if type_id == 0:
        return sum(values)
    elif type_id == 1:
        return math.prod(values)
    elif type_id == 2:
        return min(values)
    if type_id == 3:
        return max(values)
    elif type_id == 4:
        return math.prod(values)
    elif type_id == 5:
        return 1 if values[0] > values[1] else 0
    elif type_id == 6:
        return 1 if values[0] < values[1] else 0
    elif type_id == 7:
        return 1 if values[0] == values[1] else 0


def decode(bin_input, version_accumulator):
    # print("### Decode call ####")
    # print("bin_input:", bin_input, len(bin_input))

    version = int(bin_input[0:3], 2)
    version_accumulator[0] += version
    type_id = int(bin_input[3:6], 2)
    # print("version:", version, "    ", "type_id:", type_id)
    if type_id == 4:  # if literal value (i.e. type_id is 4)
        i = 0
        packets = []
        while bin_input[6+5*i] == "1":
            packets.append(bin_input[(6+5*i):(6+5*(i+1))][1:5])
            i += 1
        packets.append(bin_input[(6+5*i):(6+5*(i+1))][1:5])
        v = int("".join([*packets]), 2)
        # print("literal value:", v)
        return v, 6+5*(i+1)  # return literal_value, next_pos
    else:
        length_type_id = bin_input[6]
        # print("length_type_id:", length_type_id)
        if length_type_id == "0":  # known length
            total_length = int(bin_input[7:7+15], 2)
            # print("operator with total_length:", total_length)
            all_sub_packets_bin = bin_input[7+15:7+15+total_length]
            values, nb_bits_read = [], 0
            while nb_bits_read < total_length:
                v, pos = decode(all_sub_packets_bin[nb_bits_read:], version_accumulator)
                nb_bits_read += pos
                values.append(v)
            return perform_operation(type_id, values), 7+15+total_length
        if length_type_id == "1":
            nb_subpackets = int(bin_input[7:7+11], 2)
            # print("operator with nb_subpackets:", nb_subpackets)
            values, nb_bits_read = [], 0
            for i in range(nb_subpackets):
                v, pos = decode(bin_input[7+11+nb_bits_read:], version_accumulator)
                nb_bits_read += pos
                values.append(v)
            return perform_operation(type_id, values), 7+11+nb_bits_read


version_accumulator = [0]
values, _ = decode(bin_input, version_accumulator)
res_a = version_accumulator[0]
res_b = values

# display answers
print("answer a:", res_a)
print("answer b:", res_b)
