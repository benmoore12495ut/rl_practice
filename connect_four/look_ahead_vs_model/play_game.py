from c4_environment import *
from look_ahead_algo import *
from model_class import *
from look_ahead_with_model_fill_in import *

board = GameBoard()
algo = Algo()
model = ModelAlgo()
algo_model_fill_in = Algo_Model()

# ===================
# Play against model
# ===================
# game_still_playing = True
# player = 2
# model_player = 1
# print(board.board)
# # board.move_board_to_list()
# best_move = model.make_predictions(board.board)
# board.play_move(model_player,best_move)
# print(board.board)
# board.play_move(player,4)
# print(board.board)
# # board.move_board_to_list()
# best_move = model.make_predictions(board.board)
# board.play_move(model_player,best_move)
# print(board.board)
# board.play_move(player,4)
# print(board.board)
# # board.move_board_to_list()
# best_move = model.make_predictions(board.board)
# board.play_move(model_player,best_move)
# print(board.board)
# board.play_move(player,4)
# print(board.board)
# # board.move_board_to_list()
# best_move = model.make_predictions(board.board)
# board.play_move(model_player,best_move)
# print(board.board)
# board.play_move(player,5)
# print(board.board)
# # board.move_board_to_list()
# best_move = model.make_predictions(board.board)
# board.play_move(model_player,best_move)
# print(board.board)



# ===================
# Play against Model
# ===================
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
#         best_move = model.make_predictions(board.board)
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


# ===================
# Play against Algo model fill in
# ===================
game_still_playing = True
player = 2
game_player = 1
print(board.board)
while game_still_playing:
    if player == game_player: # user move
        move_col = input('Play move ')
        board.play_move(game_player,int(move_col))
        print(board.board)
    else: # algo move
        print_len = 60
        print_num = 1
        while print_num < print_len:
            print()
            print_num += 1
        # best_move = algo.select_best_move(board.board,game_player)+1
        best_move = algo_model_fill_in.select_best_move(board.board,game_player)+1
        board.play_move(game_player,best_move)
        print(f'algo plays: {best_move}')
        print(board.board)
    if board.game_over:
        winner = board.winner
        if winner == player:
            print('Game over - you beat the algorithm!')
        else:
            print('Game over! You lost')
        game_still_playing = False
        break
    if game_player == 2:
        game_player = 1
    else:
        game_player = 2


# ===================
# Play against look ahead
# ===================
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
#         best_move = algo.select_best_move(board.board,game_player)+1
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
