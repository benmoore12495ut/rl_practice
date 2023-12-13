import numpy as np
import pandas as pd

class GameBoard():
    def __init__(self):
        self.board = np.zeros((6,7))
        self.num_rows, self.num_columns = self.board.shape
        self.num_rows -= 1
        self.num_columns -= 1
        self.game_over = False
        self.winner = None
        self.board_list = []
        self.action_state_history = {
            1:{} # will represent all the player 1 moves and states and rewards
            ,2:{} # will represent all the player 1 moves and states and rewards
        }
        self.training_data_list=[]
        self.df_for_training = None

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

    def move_board_to_list(self):
        self.board_list = []
        for r in range(6):
            for c in range(7):
                self.board_list.append(self.board[r,c])

    def log_action_state_history(self,player,move_num,best_move):
        """
        Things to log:
         -- Key:
            1) the player
         -- values:
            1) the move number
            2) list of the 42 board values + the move column + the reward (the logging of the reward can come later)
        """
        self.move_board_to_list()
        self.board_list.append(best_move)
        self.action_state_history[player][move_num] = self.board_list

    def log_rewards(self,total_p1_moves,total_p2_moves):
        moves = {
            1:total_p1_moves
            ,2:total_p2_moves
        }
        if self.winner == None:
            rewards = {
                1:1
                ,2:1
            }
        elif self.winner == 1:
            rewards = {
                1:10000
                ,2:-10000
            }
        elif self.winner == 2:
            rewards = {
                1:-10000
                ,2:10000
            }
        # now backpropgate the rewards
        for k,v in self.action_state_history.items():
            # the initial k is the player (1 or 2)
            for k1,v1 in v.items():
                # now k1 represents the move number and v1 represents to the list of moves + the selected move by that player
                reward_mult = k1 / moves[k] # this allows the later moves to have the most weight and the earlier moves to have less weight
                reward = reward_mult * rewards[k]
                v1.append(reward)


    def rewards_to_df(self):
        for k,v in self.action_state_history.items():
            # k = player, v = dictionary of move # and list of board
            for k1,v1 in v.items():
                # k1 = move num, v1 = list of board items and rewards
                v1.append(k) # adding the player to the list
                self.training_data_list.append(v1)
        # self.df_for_training = pd.DataFrame(self.training_data_list)

        col_names = []
        for i in range(42):
            col_name = 'board_position_' + str(i)
            col_names.append(col_name)
        col_names.append('move_location')
        col_names.append('reward')
        col_names.append('moving_player')

        self.training_data_list.insert(0,col_names)

        # headers = data[0]
        # # Create the DataFrame using the rest of the data
        # df = pd.DataFrame(data[1:], columns=headers)



    def manage_csv(self, data, action='append' ,csv_file_path='~/desktop/python/reinforcement_learning_practice/connect_four/look_ahead_vs_model/model_training_data.csv'):
        """
        Manage a CSV file by either creating a new one or appending to an existing one.

        :param action: A string, either 'create' or 'append'.
        :param data: A list of dictionaries where each dictionary represents a row for 'create',
                     or a single dictionary for 'append'.
                     Keys are column names and values are the data for the columns.
        :param csv_file_path: Path to the CSV file.
        """
        headers = data[0]
        # df = pd.DataFrame(data if action == 'create' else [data])
        # df = pd.DataFrame(data if action == 'create' else data[1:])


        if action == 'create':
            # Write the DataFrame to a new CSV file, overwriting any existing file
            df = pd.DataFrame(data[1:],columns=headers)
            df.to_csv(csv_file_path, index=False)
        elif action == 'append':
            # Append the DataFrame to the CSV file
            # If the file does not exist, it will be created.
            df = pd.DataFrame(data[1:])
            df.to_csv(csv_file_path, mode='a', header=not pd.io.common.file_exists(csv_file_path), index=False)
        else:
            raise ValueError("Invalid action. Use 'create' or 'append'.")
