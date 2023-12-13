import pickle
import xgboost as xgb
import pandas as pd

class ModelAlgo():
    def __init__(self):
        self.loaded_model = None
        self.features = []
        self.board_list = []
        self.load_model()
        self.get_features()

    def load_model(self):
        with open('xgboost_regression_model.pkl', 'rb') as file:
            self.loaded_model = pickle.load(file)

    def get_features(self):
        for i in range(42):
            feature_name = 'board_position_' + str(i)
            self.features.append(feature_name)
        self.features.append('move_location')

    def move_board_to_list(self,board):
        self.board_list = []
        for r in range(6):
            for c in range(7):
                self.board_list.append(board[r,c])

    def algo_avail_positions(self,board):
        positions = []
        for c in range(7):
            if board[0,c] == 0:
                positions.append(c)
        return positions

    def make_predictions(self,board):
        avail_positions = self.algo_avail_positions(board)
        avail_positions_for_preds = []
        for a in avail_positions:
            avail_positions_for_preds.append(a+1)
        # self.move_board_to_list(board)
        best_move = 1
        best_move_points = -9999999
        # for m in range(1,8):
        for m in avail_positions_for_preds:
            self.move_board_to_list(board)
            vals = self.board_list
            vals.append(m)

            X_test = pd.DataFrame([vals],columns=self.features)
            preds = self.loaded_model.predict(X_test)

            if preds > best_move_points:
                best_move_points = preds
                best_move = m
        #     print(f'move num: {m}')
        #     print(f'prediction: {preds}')
        # print(f'Best move: {best_move}')
        # print(f'Best move points: {best_move_points}')
        return best_move


    def make_predictions_practice(self):
        best_move = 1
        best_move_points = -9999999
        for m in range(1,8):
            vals = []
            for i in range(42):
                vals.append(0)
            vals.append(m)

            X_test = pd.DataFrame([vals],columns=self.features)

            X_test.head()

            preds = self.loaded_model.predict(X_test)
            if preds > best_move_points:
                best_move_points = preds
                best_move = m
            print(f'move num: {m}')
            print(f'prediction: {preds}')
        print(f'Best move: {best_move}')
        print(f'Best move points: {best_move_points}')


# model = ModelAlgo()
# # model.load_model()
# # model.get_features()
# model.make_predictions()
