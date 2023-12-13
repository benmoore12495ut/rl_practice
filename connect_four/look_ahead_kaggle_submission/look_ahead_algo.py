import random

def is_consecutive_subsequence(small_list, big_list):
    if not small_list:
        return True
    small_index = 0
    for big_index in range(len(big_list)):
        if big_list[big_index] == small_list[small_index]:
            small_index += 1
            if small_index == len(small_list):
                return all(big_list[big_index - len(small_list) + 1 + i] == small_list[i] for i in range(len(small_list)))
    return False

def generate_sublists_with_points(x):
    # 1 in a row gives nothing
    # 2 in a row w/ 2 opens on both sides = 10
    # 2 in a row with 2 opens on one side and one open on the other = 5
    # 2 in a row with 2 opens either on one side or one on both sides = 1
    # 3 in a row with two opens = 500
    # 3 in a row with 1 open = 100
    # 4 in a row = 10000
    potential_sublists_with_points = {
        # the key means nothing, the first part of the value is the subset list and the second is the score
        1:[[0,0,x,x,0,0],10]
        ,2:[[0,x,x,0,0],5]
        ,3:[[0,0,x,x,0],5]
        ,4:[[0,x,x,0],1]
        ,5:[[0,0,x,x],1]
        ,6:[[x,x,0,0],1]
        ,7:[[0,x,x,x,0],500]
        ,8:[[x,x,x,0],100]
        ,9:[[0,x,x,x],100]
        ,10:[[x,0,x,x],100]
        ,11:[[x,x,0,x],100]
        ,12:[[x,x,x,x],10000]
    }
    return potential_sublists_with_points


def points_from_list(list_):
    rewards = {
        1:0
        ,2:0
    }
    for x in [1,2]:
        max_points = 0
        potential_sublists_with_points = generate_sublists_with_points(x)
        for k,v in potential_sublists_with_points.items():
            if is_consecutive_subsequence(v[0],list_):
                # print(f'sublist: {v[0]}')
                # print(f'points: {v[1]}')
                if v[1] > max_points:
                    max_points = v[1]
        rewards[x] = max_points

    return rewards

def algo_avail_positions(board):
    positions = []
    for c in range(7):
        if board[0,c] == 0:
            positions.append(c)
    return positions

def play_move_algo(board,player,col):
    new_board = board.copy()
    havent_move_yet = True
    r = 5
    while havent_move_yet:
        if new_board[r,col] == 0:
            new_board[r,col] = player
            havent_move_yet = False
        else:
            r -= 1
    return new_board

def find_rewards(board):
    rewards = {}
    points_awarded = {
        1:0
        ,2:0
    }
    # Check rows
    for r in range(6):
        created_list = []
        for c in range(7):
            created_list.append(board[r,c])
        rewards = points_from_list(created_list)
        points_awarded[1] += rewards[1]
        points_awarded[2] += rewards[2]

    # check columns
    for c in range(7):
        created_list = []
        for r in range(6):
            created_list.append(board[r,c])
        rewards = points_from_list(created_list)
        points_awarded[1] += rewards[1]
        points_awarded[2] += rewards[2]

    # check diagonals
    # ---- first check down to the right
    for i in range(6):
        created_list = []
        if i in (0,1):
            for j in range(6):
                val = board[j,j+i]
                created_list.append(val)
        if i == 2:
            for j in range(5):
                val = board[j,j+i]
                created_list.append(val)
        if i == 3:
            for j in range(4):
                val = board[j,j+i]
                created_list.append(val)
        if i == 4:
            for j in range(5):
                val = board[j+1,j]
                created_list.append(val)
        if i == 5:
            for j in range(4):
                val = board[j+2,j]
                created_list.append(val)
        rewards = points_from_list(created_list)
        points_awarded[1] += rewards[1]
        points_awarded[2] += rewards[2]

    # ---- then check up and to the right
    for i in range(6):
        created_list = []
        if i in (0,1):
            for j in range(6):
                val = board[5-j,j+i]
                created_list.append(val)
        if i == 2:
            for j in range(5):
                val = board[5-j,j+i]
                created_list.append(val)
        if i == 3:
            for j in range(4):
                val = board[5-j,j+i]
                created_list.append(val)
        if i == 4:
            for j in range(5):
                val = board[4-j,j]
                created_list.append(val)
        if i == 5:
            for j in range(4):
                val = board[3-j,j]
                created_list.append(val)
        rewards = points_from_list(created_list)
        points_awarded[1] += rewards[1]
        points_awarded[2] += rewards[2]

    return points_awarded

def select_best_move(board,algo_player):
    winning_move = 99
    move_dict = {}
    move_results = {}

    # =========================
    # 1) Generate all the rewards from all the moves
    # =========================
    avail_positions = algo_avail_positions(board)
    for m in avail_positions:
        new_board = play_move_algo(board,algo_player,m)
        rewards = find_rewards(new_board)
        if rewards[algo_player] >= 10000:
            winning_move = m
        move_dict[m] = [rewards,{}]
        move_results[m] = {algo_player:rewards[algo_player]}
        # check for the other play moves
        avail_positions_p2 = algo_avail_positions(new_board)
        for m2 in avail_positions_p2:
            if algo_player == 1:
                other_player = 2
            else:
                other_player = 1
            new_board_2 = play_move_algo(new_board,other_player,m2)
            rewards = find_rewards(new_board_2)
            move_dict[m][1][m2] = rewards

    # =========================
    # 2) Gather up all the points from the best moves from the other player
    # =========================
    for k,v in move_dict.items():
        other_player_best_score = 0
        other_player_best_move = -99
        other_player_moves = v[1]
        for k1, v1 in other_player_moves.items():
            if v1[other_player] >= other_player_best_score:
                other_player_best_score = v1[other_player]
                other_player_best_move = k1
                # print(f'other_player_best_move: {other_player_best_move}')
                # print(f'other_player_best_score: {other_player_best_score}')
        move_results[k][other_player] = other_player_best_score
    # print(move_dict)

    # =========================
    # 3) Select the best move
    # =========================
    best_move = 0
    best_move_points = -9999999
    best_move_options = []
    for k,v in move_results.items():
        expected_points = v[algo_player] - v[other_player]
        if expected_points >= best_move_points:
            best_move_points = expected_points
            best_move = k
            if best_move_points == 0:
                best_move_options.append(best_move)

    # print('Move results')
    # print(move_results)
    # print(f'best_move: {best_move}')
    # print(f'best_move_points: {best_move_points}')
    # print(f'best_move_options: {best_move_options}')
    # =====================
    # handle cases where there is no best move (just don't select a bad one)
    # =====================
    if best_move_points == 0:
        move_ind = random.randint(0,len(best_move_options)-1)
        # print(f'move ind: {move_ind}')
        best_move = best_move_options[move_ind]
    return best_move

def agent(observation, configuration):
    # Number of Columns on the Board.
    columns = configuration.columns
    # Number of Rows on the Board.
    rows = configuration.rows
    # Number of Checkers "in a row" needed to win.
    inarow = configuration.inarow
    # The current serialized Board (rows x columns).
    board = observation.board
    # Which player the agent is playing as (1 or 2).
    player = observation.mark

    best_move = select_best_move(board,player)

    # Return which column to drop a checker (action).
    return best_move


# ==================
# old class below
# ==================

# class Algo():
#     def __init__(self):
    #     self.dummy = 1
    #
    # def algo_avail_positions(self,board):
    #     positions = []
    #     for c in range(7):
    #         if board[0,c] == 0:
    #             positions.append(c)
    #     return positions
    #
    # def play_move_algo(self,board,player,col):
    #     new_board = board.copy()
    #     havent_move_yet = True
    #     r = 5
    #     while havent_move_yet:
    #         if new_board[r,col] == 0:
    #             new_board[r,col] = player
    #             havent_move_yet = False
    #         else:
    #             r -= 1
    #     return new_board
    #
    # def select_best_move(self,board,algo_player):
    #     winning_move = 99
    #     move_dict = {}
    #     move_results = {}
    #
    #     # =========================
    #     # 1) Generate all the rewards from all the moves
    #     # =========================
    #     avail_positions = self.algo_avail_positions(board)
    #     for m in avail_positions:
    #         new_board = self.play_move_algo(board,algo_player,m)
    #         rewards = self.find_rewards(new_board)
    #         if rewards[algo_player] >= 10000:
    #             winning_move = m
    #         move_dict[m] = [rewards,{}]
    #         move_results[m] = {algo_player:rewards[algo_player]}
    #         # check for the other play moves
    #         avail_positions_p2 = self.algo_avail_positions(new_board)
    #         for m2 in avail_positions_p2:
    #             if algo_player == 1:
    #                 other_player = 2
    #             else:
    #                 other_player = 1
    #             new_board_2 = self.play_move_algo(new_board,other_player,m2)
    #             rewards = self.find_rewards(new_board_2)
    #             move_dict[m][1][m2] = rewards
    #
    #     # =========================
    #     # 2) Gather up all the points from the best moves from the other player
    #     # =========================
    #     for k,v in move_dict.items():
    #         other_player_best_score = 0
    #         other_player_best_move = -99
    #         other_player_moves = v[1]
    #         for k1, v1 in other_player_moves.items():
    #             if v1[other_player] >= other_player_best_score:
    #                 other_player_best_score = v1[other_player]
    #                 other_player_best_move = k1
    #                 # print(f'other_player_best_move: {other_player_best_move}')
    #                 # print(f'other_player_best_score: {other_player_best_score}')
    #         move_results[k][other_player] = other_player_best_score
    #     # print(move_dict)
    #
    #     # =========================
    #     # 3) Select the best move
    #     # =========================
    #     best_move = 0
    #     best_move_points = -9999999
    #     best_move_options = []
    #     for k,v in move_results.items():
    #         expected_points = v[algo_player] - v[other_player]
    #         if expected_points >= best_move_points:
    #             best_move_points = expected_points
    #             best_move = k
    #             if best_move_points == 0:
    #                 best_move_options.append(best_move)
    #
    #     # print('Move results')
    #     # print(move_results)
    #     # print(f'best_move: {best_move}')
    #     # print(f'best_move_points: {best_move_points}')
    #     # print(f'best_move_options: {best_move_options}')
    #     # =====================
    #     # handle cases where there is no best move (just don't select a bad one)
    #     # =====================
    #     if best_move_points == 0:
    #         move_ind = random.randint(0,len(best_move_options)-1)
    #         # print(f'move ind: {move_ind}')
    #         best_move = best_move_options[move_ind]
    #     return best_move
    #
    #
    # def find_rewards(self,board):
    #     self.rewards = {}
    #     points_awarded = {
    #         1:0
    #         ,2:0
    #     }
    #     # Check rows
    #     for r in range(6):
    #         created_list = []
    #         for c in range(7):
    #             created_list.append(board[r,c])
    #         rewards = points_from_list(created_list)
    #         points_awarded[1] += rewards[1]
    #         points_awarded[2] += rewards[2]
    #
    #     # check columns
    #     for c in range(7):
    #         created_list = []
    #         for r in range(6):
    #             created_list.append(board[r,c])
    #         rewards = points_from_list(created_list)
    #         points_awarded[1] += rewards[1]
    #         points_awarded[2] += rewards[2]
    #
    #     # check diagonals
    #     # ---- first check down to the right
    #     for i in range(6):
    #         created_list = []
    #         if i in (0,1):
    #             for j in range(6):
    #                 val = board[j,j+i]
    #                 created_list.append(val)
    #         if i == 2:
    #             for j in range(5):
    #                 val = board[j,j+i]
    #                 created_list.append(val)
    #         if i == 3:
    #             for j in range(4):
    #                 val = board[j,j+i]
    #                 created_list.append(val)
    #         if i == 4:
    #             for j in range(5):
    #                 val = board[j+1,j]
    #                 created_list.append(val)
    #         if i == 5:
    #             for j in range(4):
    #                 val = board[j+2,j]
    #                 created_list.append(val)
    #         rewards = points_from_list(created_list)
    #         points_awarded[1] += rewards[1]
    #         points_awarded[2] += rewards[2]
    #
    #     # ---- then check up and to the right
    #     for i in range(6):
    #         created_list = []
    #         if i in (0,1):
    #             for j in range(6):
    #                 val = board[5-j,j+i]
    #                 created_list.append(val)
    #         if i == 2:
    #             for j in range(5):
    #                 val = board[5-j,j+i]
    #                 created_list.append(val)
    #         if i == 3:
    #             for j in range(4):
    #                 val = board[5-j,j+i]
    #                 created_list.append(val)
    #         if i == 4:
    #             for j in range(5):
    #                 val = board[4-j,j]
    #                 created_list.append(val)
    #         if i == 5:
    #             for j in range(4):
    #                 val = board[3-j,j]
    #                 created_list.append(val)
    #         rewards = points_from_list(created_list)
    #         points_awarded[1] += rewards[1]
    #         points_awarded[2] += rewards[2]
    #
    #     return points_awarded
