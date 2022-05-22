from pyprojroot import here
data_dir = here("data")


# the level information contained in the node is deprecated and unmaintained...
# too hard to remove now as change the structure indexes
# -> next time create a class for the node instead of an ad-hoc structure from a list
# it makes the maintenance easier in case specs have to change
def create_node(inputs, parent_node=None, level=0, leaf_side=None):
    i, values = 0, []
    cur_node = [level, None, [None, None], parent_node, leaf_side]  # start cur_node
    while i < len(inputs):
        if inputs[i] == "[":
            cur_node[2][0], pos = create_node(inputs[(i+1):], cur_node, level + 1, "left")
            i += pos
            cur_node[2][1], pos = create_node(inputs[(i+1):], cur_node, level + 1, "right")
            i += pos
            return cur_node, i+2
        elif inputs[i] == ",":
            cur_node[1] = int("".join(values))
            return cur_node, i+1
        elif inputs[i] == "]":
            if len(values) == 0:
                return cur_node, i+1
            else:
                cur_node[1] = int("".join(values))
                return cur_node, i+1
        else:
            values.append(inputs[i])
        i += 1
    return cur_node, 0


def write_node(node):
    if node[1] is None:
        return "".join(["[", write_node(node[2][0]), ",", write_node(node[2][1]), "]"])
    else:
        return str(node[1])


def add_value_rec(node, v, side_to, side_from, has_switched):
    if node[1] is not None:
        node[1] += v
        return "done"
    if side_to == side_from:   # go up if possible
        return add_value_rec(node[3], v, side_to, node[4], has_switched) if node[3] is not None else "fail"
    else:  # go down
        k = 0 if side_to == "left" else 1
        if not has_switched:
            side_to = "left" if side_to == "right" else "right"
        return add_value_rec(node[2][k], v, side_to, "up", True)


def explode(node):
    level, parent_node, cur_side = node[0], node[3], node[4]
    cur_value_left, cur_value_right = node[2][0][1], node[2][1][1]
    # left value to be added
    # go down left once, then always right
    # never go where you came from
    add_value_rec(parent_node, cur_value_left, "left", cur_side, False)
    add_value_rec(parent_node, cur_value_right, "right", cur_side, False)  # same with right
    return [level, 0, (None, None), parent_node, cur_side]


def split(node):
    # not sure the parent is given right
    left_child = [node[0] + 1, node[1]//2, [None, None], node, "left"]
    right_child = [node[0] + 1, node[1]//2 + 1, [None, None], node, "right"]
    return [node[0], None, [left_child, right_child], node[3], node[4]]


def do_explosions(node, level=0):
    left_response, right_response = None, None
    if node[2][0] is not None:
        left_response = do_explosions(node[2][0], level + 1)
        if left_response == "restart":
            return "restart"
    if node[2][1] is not None:
        right_response = do_explosions(node[2][1], level + 1)
        if right_response == "restart":
            return "restart"
    if left_response == right_response == "explode":
        node[3][2][0 if node[4] == "left" else 1] = explode(node)
        return "restart"
    if node[2][0] is None and node[2][1] is None and level > 4:  # explode parent!
        return "explode"
    return "done"


def do_splits(node):
    if node[1] is not None and node[1] > 10:
        # left_child = [node[0] + 1, node[1]//2, [None, None], node[3][2][0 if node[4] == "left" else 1], "left"]
        # right_child = [node[0] + 1, node[1]//2 + 1, [None, None], node[3][2][0 if node[4] == "left" else 1], "right"]
        # node[3][2][0 if node[4] == "left" else 1] = [node[0], None, [left_child, right_child], node[3], node[4]]
        node[3][2][0 if node[4] == "left" else 1] = split(node)
        return "restart"
    if node[1] is None:
        response = do_splits(node[2][0])
        return response if response == "restart" else do_splits(node[2][1])
    return "done"


def reduce(tree):
    i = 0
    while i < 10:
        tree_str = write_node(tree)
        res = do_explosions(tree)
        if res == "restart":
            print("after explosion:", write_node(tree))
            continue
        tree_str = write_node(tree)
        res = do_splits(tree)
        if res == "done":
            # explosions done THEN splits done without any change
            break
        else:
            print("after split:", write_node(tree))
        i += 1
        if i == 10:
            break


# inputs = "[[6,[5,[4,[3,2]]]],1]"
# inputs = "[[[[[9,8],1],2],3],4]"
# inputs = "[[4,5],2]"
# inputs = "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
inputs1 = "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]"
inputs2 = "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]"
inputs = "[" + inputs1 + "," + inputs2 + "]"
# # inputs = "[1,2]"
# # inputs = "[[1,2],3]"
# # inputs = "[1,[2, 3]]"
# print(inputs)
tree = create_node(inputs)[0]
# # print(tree)
# print(write_node(tree))
reduce(tree)
print(write_node(tree))

print(write_node(tree[2][1]))

print(tree[2][1])

# load input file
# input_file = data_dir / "test18.txt"
# # input_file = data_dir / "input18.txt"
# with open(input_file, 'r') as f:
#     inputs = [e.replace("\n", "") for e in f.readlines()]

# print(inputs[0])

# tree = create_node(inputs[0])[0]
# for i in range(1, 2):
# for i in range(1, len(inputs)):
#     n = create_node(inputs[i])[0]
#     new_tree = [-1, None, [tree, n], None, None]
#     new_tree[2][0][3], new_tree[2][1][3] = new_tree, new_tree
#     new_tree[2][0][4], new_tree[2][1][4] = "left", "right"
#     tree = new_tree

# print(write_node(tree))
# reduce(tree)
# print(write_node(tree))


# print(m)

# node = [v or None, None or [left_child, right_child], parent]

# display answers
# print("answer a:", res_a)
# print("answer b:", res_b)
