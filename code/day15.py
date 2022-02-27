import math
from heapq import heappop, heappush
from pyprojroot import here
data_dir = here("data")

# load input file
# input_file = data_dir / "test15.txt"
input_file = data_dir / "input15.txt"
with open(input_file, 'r') as f:
    maze = [[int(c) for c in e.replace("\n", "")] for e in f.readlines()]


# expand horizontally
big_maze_tmp = []
for l in maze:
    cur_l = []
    for i in range(5):
        cur_l.extend([(e + i) % 9 if (e + i) % 9 != 0 else 9 for e in l])
    big_maze_tmp.append(cur_l)

# expand vertically
big_maze = []
for i in range(5):
    for l in big_maze_tmp:
        big_maze.append([(e + i) % 9 if (e + i) % 9 != 0 else 9 for e in l])


# orthogonal only
def get_neighbors(m, i, j):
    n = []
    shifts = [[-1, 0], [0, -1], [0, 1], [1, 0]]
    # shifts = [[0, 1], [1, 0]]  # only allow direct path !?
    for k, l in shifts:
        if 0 <= i+k < len(m) and 0 <= j+l < len(m[0]):
            n.append((i+k, j+l))
    return n


# raoul homemade version of Dijkstra
def find_shortest_path(maze, queue):
    explored_tiles = set()
    counter = 0
    while True:
        # new data structure ! any element added through heappush will be first if smallest
        # any element removed through heappop will be the smallest one (assuming elements
        # were added with heappush)
        cheapest_tile_desc = heappop(queue)
        # if counter % 1000 == 0:
        #     print("debug: ", counter, cheapest_tile_desc[1], cheapest_tile_desc[0])

        # get all their non-explored neighbors from last explored tile
        x_i, x_j = cheapest_tile_desc[1]
        neighbors_tiles = [t for t in get_neighbors(maze, x_i, x_j) if t not in explored_tiles]

        # check if a neighbor is the end of the maze, stop if so
        for nt in neighbors_tiles:
            new_path_desc = (cheapest_tile_desc[0] + maze[nt[0]][nt[1]], nt)
            if nt == (len(maze)-1, len(maze[0])-1):  # that's the end of the maze!
                return new_path_desc
            else:
                explored_tiles.add(nt)
                heappush(queue, new_path_desc)

        counter += 1


queue = [(0, (0, 0))]  # queue is a list of (cur_cost, tile) elements, tile is a position tuple (i, j)
res_a = find_shortest_path(maze, queue)[0]
queue = [(0, (0, 0))]
res_b = find_shortest_path(big_maze, queue)[0]

# display answers
print("answer a:", res_a)
print("answer b:", res_b)
