# import copy
from pyprojroot import here
data_dir = here("data")


# from day3
def get_col(i, l):
    return [e[i] for e in l]


# from day3
def most_common(l):
    # returns 1 if ties (oxygen rule, day 3)
    if l.count(0) <= l.count(1):
        return 1
    return 0


def tick_in_board(d, board):
    for i, r in enumerate(board):
        for j, e in enumerate(r):
            if e == d:
                board[i][j] = None


def check_win(board):
    if max([r.count(None) for r in board]) == len(board[0]):
        return True
    if max([get_col(i, board).count(None) for i in range(len(board[0]))]) == len(board):
        return True
    return False


def sum_board(board):
    return sum([e for r in board for e in r if e is not None])


# load input file
# file = open('test4a.txt', 'r')
file = open(data_dir / 'input4.txt', 'r')
all_inputs = [e.replace('\n', '').split(" ") for e in file.readlines()]
drawn = [int(e) for e in all_inputs[0][0].split(",")]

# part a
boards = list()
cur_board = list()
for r in all_inputs[2:]:
    if len(r) == 1 and r[0] == '':
        boards.append(cur_board)
        cur_board = list()
        continue
    cur_board.append([int(e) for e in r if e != ''])
boards.append(cur_board)


def play(boards, drawn):
    for d in drawn:
        for b in boards:
            tick_in_board(d, b)
            if check_win(b):
                return sum_board(b) * d


res_a = play(boards, drawn)

# part b
boards = list()
cur_board = list()
for r in all_inputs[2:]:
    if len(r) == 1 and r[0] == '':
        boards.append(cur_board)
        cur_board = list()
        continue
    cur_board.append([int(e) for e in r if e != ''])
boards.append(cur_board)


def play(boards, drawn):
    won_boards_ind = list()
    for d in drawn:
        for b_i, b in enumerate(boards):
            if b_i in won_boards_ind:
                continue
            tick_in_board(d, b)
            if check_win(b):
                won_boards_ind.append(b_i)
                if len(won_boards_ind) == len(boards):
                    return sum_board(b) * d


res_b = play(boards, drawn)

# display results
print("answer a:", res_a)
print("answer b:", res_b)
