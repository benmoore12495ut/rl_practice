import numpy as np
def adjust_board(board):
    new_board = np.array(board).reshape(6, 7)
    return new_board 


board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

new_board = adjust_board(board)

print(new_board)
