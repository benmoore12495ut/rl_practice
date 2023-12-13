from c4_environment_ import *
from look_ahead_algo import *

board = GameBoard()
# algo = Algo()


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
        best_move = select_best_move(board.board,game_player)+1
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
