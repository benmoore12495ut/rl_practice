import pandas as pd
import pickle
import xgboost as xgb
import time


# ========================
# User inputs
add_sample_weight = 1
include_swapped_2s = 1
print('**Params**')
print(f'sample weight: {add_sample_weight}')
print(f'include_swapped_2s weight: {include_swapped_2s}')
print()
# =======================

df = pd.read_csv('~/desktop/python/reinforcement_learning_practice/connect_four/look_ahead_vs_model/model_training_data.csv')

print(f'Length of training data pre agg: {len(df)}')

features = []
for col in df.columns:
    if col[:5] == 'board':
        features.append(col)
features.append('move_location')

label = 'reward'

def swap_values(x):
    if x == 1:
        return 2
    elif x == 2:
        return 1
    else:
        return x

def prep_for_training():
    df_1s = df.loc[df['moving_player']==1]

    if include_swapped_2s==1:
        df_2s = df.loc[df['moving_player']==2]
        df_2s_swapped = df_2s.applymap(swap_values)
        df_with_2s_swapped = pd.concat([df_1s,df_2s_swapped])
        df_for_training = df_with_2s_swapped.groupby(features).agg(
                                                     reward=('reward','mean')
                                                     ,num_instances=('moving_player','sum')).reset_index()
        print(f'Length of training data post agg with 1s and 2s swapped: {len(df_for_training)}')

    else: # just play with half the data set
        df_for_training = df_1s.groupby(features).agg(
                                                 reward=('reward','mean')
                                                 ,num_instances=('moving_player','sum')).reset_index()
        print(f'Length of training data post agg & 1s: {len(df_for_training)}')

    return df_for_training


df_for_training = prep_for_training()

training_start_time = time.time()
xg_reg = xgb.XGBRegressor(objective ='reg:squarederror'
#                           , colsample_bytree = 0.3
#                           , learning_rate = 0.1
#                           , max_depth = 5
#                           , alpha = 10
#                           , n_estimators = 10
                         )

X_train = df_for_training[features]
y_train = df_for_training[label]

# Extract sample weights
sample_weights = df_for_training['num_instances']

if add_sample_weight==1:
    xg_reg.fit(X_train, y_train, sample_weight=sample_weights)
else:
    xg_reg.fit(X_train, y_train)


curr_time = time.time()
training_time = curr_time - training_start_time
print(f'Trained Model in {round(training_time,3)} seconds')


# Save the model to a file
with open('xgboost_regression_model.pkl', 'wb') as file:
    pickle.dump(xg_reg, file)
print('Saved file')
