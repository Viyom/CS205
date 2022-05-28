from copy import deepcopy
import pandas as pd
from sklearn.model_selection import train_test_split

final_best_features = []
final_best_score = 0

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
  best_score_feature_index = -1
  for index, val in enumerate(X_train[0]):
    if index not in best_feature_list:
      best_feature_list_ = deepcopy(best_feature_list)
      best_feature_list_.append(index)
      y_pred = predict(X_train[:,best_feature_list_], Y_train, X_test[:,best_feature_list_])
      score = evaluate(y_pred, Y_test)
      if score > best_score:
        best_score = score
        best_score_feature_index = index
  return best_score_feature_index

def forward_selection(X_train, X_test, Y_train, Y_test):
  global final_best_features
  global final_best_score
  best_feature_list = []
  for val in X_train[0]:
    next_best = find_next_best_feature_index(best_feature_list, X_train, X_test, Y_train, Y_test)
    best_feature_list.append(next_best)
    y_pred = predict(X_train[:,best_feature_list], Y_train, X_test[:,best_feature_list])
    score = evaluate(y_pred, Y_test)
    if score > final_best_score:
      final_best_score = score
      final_best_features = deepcopy(best_feature_list)
    print ("Correct predictions:", score, "Total predictions:", len(y_pred), "Features selected:", best_feature_list)

def find_next_worst_feature_val(best_feature_list, X_train, X_test, Y_train, Y_test):
  best_score = 0
  worst_score_feature_val = -1
  for val in best_feature_list:
    best_feature_list_ = deepcopy(best_feature_list)
    best_feature_list_.remove(val)
    y_pred = predict(X_train[:,best_feature_list_], Y_train, X_test[:,best_feature_list_])
    score = evaluate(y_pred, Y_test)
    if score > best_score:
      best_score = score
      worst_score_feature_val = val
  return worst_score_feature_val

def backward_elimination(X_train, X_test, Y_train, Y_test):
  global final_best_features
  global final_best_score
  best_feature_list = list(range(0,len(X_train[0])))
  while len(best_feature_list) != 0:
    y_pred = predict(X_train[:,best_feature_list], Y_train, X_test[:,best_feature_list])
    score = evaluate(y_pred, Y_test)
    if score > final_best_score:
      final_best_score = score
      final_best_features = deepcopy(best_feature_list)
    print ("Correct predictions:", score, "Total predictions:", len(y_pred), "Features selected:", best_feature_list)
    next_worst = find_next_worst_feature_val(best_feature_list, X_train, X_test, Y_train, Y_test)
    best_feature_list.remove(next_worst)

def get_input():
  dataset = int(input("Choose the dataset to be evaluated (Enter 1 or 2)\n1) Small\n2) Large (WARNING: Since the dataset is large it will take much more time to execute)\nEnter: "))
  if dataset == 1:
    dataset = "CS205_SP_2022_SMALLtestdata__74.txt"
  if dataset == 2:
    dataset = "CS205_SP_2022_Largetestdata__14.txt"
  search_technique = int(input("Choose the search technique (Enter 1 or 2)\n1) Forward Selection\n2) Backward Elimination\nEnter: "))
  return dataset, search_technique

dataset, search_technique = get_input()
X, Y = load_dataset(dataset)
normalize(X)
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.20, random_state = 2)
if search_technique == 1:
  forward_selection(X_train, X_test, Y_train, Y_test)
if search_technique == 2:
  backward_elimination(X_train, X_test, Y_train, Y_test)
print ("Final best set of features:", final_best_features, "Maximum correct predictions:", final_best_score)
