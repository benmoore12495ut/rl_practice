import numpy as np

class GameBoard():
    def __init__(self):
        self.board = np.zeros((6,7))
        self.num_rows, self.num_columns = self.board.shape
        self.num_rows -= 1
        self.num_columns -= 1
        self.game_over = False
        self.winner = None

    def play_move(self,player,col):
        playing_col = col - 1
        if self.board[0,playing_col] != 0:
            # print('column full, try again')
            pass
        else:
            havent_move_yet = True
            r = 5
            while havent_move_yet:
                if self.board[r,playing_col] == 0:
                    self.board[r,playing_col] = player
                    havent_move_yet = False
                else:
                    r -= 1
        self.check_for_winner()
        # print(self.board)

    def avail_positions(self):
        positions = []
        for c in range(7):
            if self.board[0,c] == 0:
                positions.append(c)
        return positions


    def check_for_winner(self):
        # Check rows
        found_a_match = False
        for r in range(self.num_rows+1):
            num_in_a_row = 0
            for c in range(1,self.num_columns+1):
                if self.board[r,c] != 0 and self.board[r,c-1] == self.board[r,c]:
                    if num_in_a_row == 0:
                        num_in_a_row = 2
                    else:
                        num_in_a_row += 1
                    if num_in_a_row == 4:
                        found_a_match = True
                        self.winner = self.board[r,c]
                else:
                    num_in_a_row = 0
        if found_a_match:
            self.game_over = True


        # Check columns
        found_a_match = False
        for c in range(self.num_columns+1):
            num_in_a_row = 0
            for r in range(1,self.num_rows+1):
                if self.board[r,c] != 0 and self.board[r-1,c] == self.board[r,c]:
                    if num_in_a_row == 0:
                        num_in_a_row = 2
                    else:
                        num_in_a_row += 1
                    if num_in_a_row == 4:
                        found_a_match = True
                        self.winner = self.board[r,c]
                else:
                    num_in_a_row = 0
        if found_a_match:
            self.game_over = True

        # Check down to the right diagonal
        found_a_match = False
        for c in range(4):
            for r in range(3):
                if self.board[r,c] == self.board[r+1,c+1] == self.board[r+2,c+2] == self.board[r+3,c+3] != 0:
                    found_a_match = True
                    self.winner = self.board[r,c]
        if found_a_match:
            self.game_over = True

        # Check down to the left diagonal
        found_a_match = False
        for c in range(3,7):
            for r in range(3):
                if self.board[r,c] == self.board[r+1,c-1] == self.board[r+2,c-2] == self.board[r+3,c-3] != 0:
                    found_a_match = True
                    self.winner = self.board[r,c]
        if found_a_match:
            self.game_over = True

        # if all moves are filled in, return game over
        num_open_spaces = 0
        for c in range(self.num_columns+1):
            for r in range(self.num_rows+1):
                if self.board[r,c] == 0:
                    num_open_spaces += 1
        if num_open_spaces == 0:
            self.game_over = True
