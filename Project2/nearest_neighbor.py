from copy import deepcopy
import pandas as pd
from sklearn.model_selection import train_test_split

def load_dataset(input_file):
  df = pd.read_csv(input_file, delim_whitespace=True, header=None)
  Y = df.iloc[:,0].values.astype(int)
  X = df.iloc[:,1:].values.astype(float)
  return X, Y

def calc_dist(x_train, x_test):
  dist = 0
  for index, val in enumerate(x_train):
    dist += (x_train[index] - x_test[index])**2
  return dist**(1/2)

def predict(X_train, Y_train, X_test):
  Y_pred = []
  for x_test in X_test:
    min_dist = float("inf")
    prediction = -1
    for index, x_train in enumerate(X_train):
      distance = calc_dist(x_train, x_test)
      if distance < min_dist:
        min_dist = distance
        prediction = Y_train[index]
    Y_pred.append(prediction)
  return Y_pred

def evaluate(Y_pred, Y_test):
  correct_pred = 0
  for index, val in enumerate(Y_pred):
    if Y_pred[index] == Y_test[index]:
      correct_pred += 1
  return correct_pred

def normalize(X):
  for list_index, list_ in enumerate(X):
    max_ = float("-inf")
    min_ = float("inf")
    for item in list_:
      if item > max_:
        max_= item
      if item < min_:
        min_ = item
    for item_index, item in enumerate(list_):
      X[list_index][item_index] = (item - min_)/(max_ -  min_)

def find_next_best_feature_index(best_feature_list, X_train, X_test, Y_train, Y_test):
  best_score = 0
  best_score_index = -1
  for index, val in enumerate(X_train[0]):
    if index not in best_feature_list:
      best_feature_list_ = deepcopy(best_feature_list)
      best_feature_list_.append(index)
      y_pred = predict(X_train[:,best_feature_list_], Y_train, X_test[:,best_feature_list_])
      score = evaluate(y_pred, Y_test)
      if score > best_score:
        best_score = score
        best_score_index = index
  return best_score_index # Return best score from here only (Can be used for testing as well)

def forward_selection(X_train, X_test, Y_train, Y_test):
  best_feature_list = []
  for val in X_train[0]:
    next_best = find_next_best_feature_index(best_feature_list, X_train, X_test, Y_train, Y_test)
    best_feature_list.append(next_best)
    y_pred = predict(X_train[:,best_feature_list], Y_train, X_test[:,best_feature_list])
    score = evaluate(y_pred, Y_test)
    print ("Correct predictions:", score, "Total predictions:", len(y_pred), "Features selected:", best_feature_list)

X, Y = load_dataset('CS205_SP_2022_SMALLtestdata__74.txt')
normalize(X)
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.20, random_state = 2)
forward_selection(X_train, X_test, Y_train, Y_test)
