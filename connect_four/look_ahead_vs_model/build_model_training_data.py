
# =============================
# Look ahead plays against itself to create training data
# =============================
from c4_environment import *
from look_ahead_algo import *
import time

# algo_0 = Algo(0.2,1) # explore, game player
# algo_4 = Algo(0.2,2)

winner_log = {
    1:0
    ,2:0
    ,0:0
}

def play_training_game(game_num):
    game_still_playing = True
    player = 1
    board = GameBoard()
    move_num = 0
    moves = {
        1:0
        ,2:0
    }

    while game_still_playing:
        if board.game_over:
            winner = board.winner
            try:
                if winner == 1:
                    # print('Winner = Algo 1')
                    winner_log[winner]+= 1
                else:
                    # print('Winner = Algo 2')
                    winner_log[winner]+= 1
            except:
                # print('Tie')
                winner_log[0] += 1
            # print(board.board)
            board.log_rewards(moves[1],moves[2])
            board.rewards_to_df()
            # print(board.training_data_list)
            # print(pd.DataFrame(board.training_data_list))
            if game_num == 1:
                board.manage_csv(board.training_data_list,action='create')
            else:
                board.manage_csv(board.training_data_list,action='append')
            # print(board.df_for_training.head(50))
            # print(board.action_state_history)
            game_still_playing = False
            break

        if player == 1:
            player_ = algo_0.game_player
            best_move = algo_0.select_best_move(board.board,player_,move_num)+1
        else: # player = 2
            player_ = algo_4.game_player
            best_move = algo_4.select_best_move(board.board,player_,move_num)+1

        moves[player_] += 1
        move_num = moves[player_]
        board.log_action_state_history(player_,move_num,best_move)
        board.play_move(player_,best_move)
        move_num += 1
        # print(board.action_state_history)


        if player == 2:
            player = 1
        else:
            player = 2

# num_games = 50
# target_num_rows = 1000000
target_num_rows = 400000
# target_num_rows = 500
rows_per_game = 25
num_games = target_num_rows / rows_per_game
print(f'Total num games: {num_games}')
curr_game = 2
start_time = time.time()
last_10_games_start_time = time.time()
while curr_game <= num_games:
    a_0_explore = random.randint(0,6) / 10
    a_4_explore = random.randint(0,6) / 10
    # determine how much explore to have
    algo_0 = Algo(a_0_explore,1) # explore, game player
    algo_4 = Algo(a_4_explore,2)
    # play the game
    if curr_game % 10 ==0:
        print()
        print(f'Current game: {curr_game}')
        print(f'algo 0 explore: {a_0_explore}')
        print(f'algo 4 explore: {a_4_explore}')
        total_min = round(((time.time() - start_time)/60),1)
        print(f'Total min: {total_min}')
        print(f'Last 10 games min: {round(((time.time() - last_10_games_start_time)/60),1)}')
        print(f'completed {round(curr_game*100 / num_games,1)}% of games')
        # min_remaining = total_min * (num_games)
        # print(f'expected time remaining: {} hours, {} min')
        print(winner_log)
        last_10_games_start_time = time.time()
    play_training_game(curr_game)
    curr_game +=1
print('** FINAL WINNER LOG **')
print(winner_log)









# =============================
# Helper code below to play against a human
# =============================

# from c4_environment_ import *
# from look_ahead_algo import *
#
# board = GameBoard()
# # algo = Algo()
#
#
# game_still_playing = True
# player = 2
# game_player = 1
# print(board.board)
# while game_still_playing:
#     if player == game_player: # user move
#         move_col = input('Play move ')
#         board.play_move(game_player,int(move_col))
#         print(board.board)
#     else: # algo move
#         print_len = 60
#         print_num = 1
#         while print_num < print_len:
#             print()
#             print_num += 1
#         # best_move = algo.select_best_move(board.board,game_player)+1
#         best_move = select_best_move(board.board,game_player)+1
#         board.play_move(game_player,best_move)
#         print(f'algo plays: {best_move}')
#         print(board.board)
#     if board.game_over:
#         winner = board.winner
#         if winner == player:
#             print('Game over - you beat the algorithm!')
#         else:
#             print('Game over! You lost')
#         game_still_playing = False
#         break
#     if game_player == 2:
#         game_player = 1
#     else:
#         game_player = 2
