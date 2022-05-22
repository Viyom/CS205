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

X, Y = load_dataset('CS205_SP_2022_SMALLtestdata__74.txt')
normalize(X)
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.20, random_state = 2)
Y_pred = predict(X_train, Y_train, X_test)
correct_pred = evaluate(Y_pred, Y_test)
print ("Correct predictions:", correct_pred, "Total predictions:", len(Y_pred))
