import collections
from pyprojroot import here
data_dir = here("data")

players_pos = [8, 10]
players_score = [0, 0]
dice_counter, dice_next_roll = 0, 1
playing_player = 0

while players_score[0] < 1000 and players_score[1] < 1000:
    cur_dice_tot = 0
    for i in range(3):
        cur_dice_tot += dice_next_roll
        dice_next_roll = dice_next_roll % 100 + 1
        dice_counter += 1
    players_pos[playing_player] = (players_pos[playing_player] + cur_dice_tot - 1) % 10 + 1
    players_score[playing_player] += players_pos[playing_player]
    playing_player = (playing_player + 1) % 2

res_a = min(players_score[0], players_score[1]) * dice_counter


roll_universe = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
universes_count = collections.defaultdict(lambda: 0)
universes_count[(0, (8, 10), (0, 0))] = 1
positions = [0, 0]
scores = [0, 0]
counter = 0
p1_wins, p2_wins = 0, 0
while len(universes_count) > 0:
    # we explore the universes from low scores to higher ones (it's strictly increasing when expanding)
    board, nb_universes = min(universes_count.items(), key=lambda x: x[0][2][0] + x[0][2][1])
    del universes_count[board]
    # if counter % 1000 == 0:
    #     print(board[2][0] + board[2][1])
    player, (positions[0], positions[1]), (scores[0], scores[1]) = board
    if scores[0] >= 21:
        p1_wins += nb_universes
    elif scores[1] >= 21:
        p2_wins += nb_universes
    else:
        for k, v in roll_universe.items():
            cur_pos = (positions[player] + k - 1) % 10 + 1
            cur_sc = scores[player] + cur_pos
            if player == 0:
                cur_univ = (1, (cur_pos, positions[1]), (cur_sc, scores[1]))
            else:
                cur_univ = (0, (positions[0], cur_pos), (scores[0], cur_sc))
            universes_count[cur_univ] += v * nb_universes
    counter += 1

res_b = max(p1_wins, p2_wins)

# display answers
print("answer a:", res_a)
print("answer b:", res_b)
