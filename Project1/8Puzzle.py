from copy import deepcopy
import heapq

class eight_puzzle:
  state = [[0,0,0],[0,0,0],[0,0,0]]
  g = -1
  h = -1
  solution = []
  def __lt__(self, other):
    return self.g + self.h < other.g + other.h

## Heuristic numbers:
## 1)Uniform Cost Search
## 2)A* with the Misplaced Tile heuristic
## 3)A* with the Manhattan Distance heuristic
heuristic = 1

total_nodes_expanded = 0
visited_nodes_state = []
max_queue_size = 0

sampleProblems = []
sampleProblems.append([[1,2,3],[4,5,6],[7,8,0]])
sampleProblems.append([[1,2,3],[4,5,6],[0,7,8]])
sampleProblems.append([[1,2,3],[5,0,6],[4,7,8]])
sampleProblems.append([[1,3,6],[5,0,2],[4,7,8]])
sampleProblems.append([[1,3,6],[5,0,7],[4,8,2]])
sampleProblems.append([[1,6,7],[5,0,3],[4,8,2]])
sampleProblems.append([[7,1,2],[4,8,5],[6,3,0]])
sampleProblems.append([[0,7,2],[4,6,1],[3,5,8]])

def calculate_h(node):
  h = 0
  if heuristic == 1:
    h = 0
  if heuristic == 2:
    for i,row in enumerate(node.state):
      for j,val in enumerate(row):
        if val != 0  and val != i*3+j+1:
          h += 1
  if heuristic == 3:
    for i,row in enumerate(node.state):
      for j,val in enumerate(row):
        actual_i, actual_j = (val-1)//3, (val-1)%3
        if actual_j == -1:
          actual_i, actual_j = 2,2
        h += abs(actual_i - i) + abs(actual_j - j)
  return h
  
def get_input():
  problem = eight_puzzle()
  for i in range(1,9):
    print (str(i)+")",sampleProblems[i-1])
  problem_selection = int(input("Choose number from the above sample problems or select 0 to input custom problem:"))
  if problem_selection == 0:
    row1 = input("Enter first row (space separated):")
    problem.state[0] = [int(x) for x in row1.split()]
    row2 = input("Enter second row (space separated):")
    problem.state[1] = [int(x) for x in row2.split()]
    row3 = input("Enter third row (space separated):")
    problem.state[2] = [int(x) for x in row3.split()]
  else:
    problem.state = sampleProblems[problem_selection-1]
  global heuristic
  heuristic = int(input("Choose one of the following (Type 1, 2 or 3)\n1) Uniform Cost Search\n2) A* with the Misplaced Tile heuristic\n3) A* with the Manhattan Distance heuristic\nEnter:"))
  problem.g = 0
  problem.h = calculate_h(problem)
  return problem

def remove_front(nodes):
  return heapq.heappop(nodes)

def goal_test(node):
  test_success = True
  for i,row in enumerate(node.state):
    for j,val in enumerate(row):
      if val == i*3+j+1 or (i==2 and j==2 and val==0):
        continue
      else:
        test_success = False
  return test_success

def expand(node):
  global total_nodes_expanded
  total_nodes_expanded += 1
  expanded_nodes = []
  i_cord, j_cord = 0, 0
  for i,row in enumerate(node.state):
    for j,val in enumerate(row):
      if val == 0:
        i_cord = i
        j_cord = j
        break
  if j_cord - 1 > -1:
    left = eight_puzzle()
    left.state = deepcopy(node.state)
    left.state[i_cord][j_cord-1], left.state[i_cord][j_cord] = left.state[i_cord][j_cord], left.state[i_cord][j_cord-1]
    left.g = node.g + 1
    left.h = calculate_h(left)
    left.solution = deepcopy(node.solution)
    left.solution.append("Left")
    if left.state not in visited_nodes_state:
      visited_nodes_state.append(left.state)
      expanded_nodes.append(left)

  if j_cord + 1 < 3:
    right = eight_puzzle()
    right.state = deepcopy(node.state)
    right.state[i_cord][j_cord+1], right.state[i_cord][j_cord] = right.state[i_cord][j_cord], right.state[i_cord][j_cord+1]
    right.g = node.g + 1
    right.h = calculate_h(right)
    right.solution = deepcopy(node.solution)
    right.solution.append("Right")
    if right.state not in visited_nodes_state:
      visited_nodes_state.append(right.state)
      expanded_nodes.append(right)

  if i_cord - 1 > -1:
    up = eight_puzzle()
    up.state = deepcopy(node.state)
    up.state[i_cord-1][j_cord], up.state[i_cord][j_cord] = up.state[i_cord][j_cord], up.state[i_cord-1][j_cord]
    up.g = node.g + 1
    up.h = calculate_h(up)
    up.solution = deepcopy(node.solution)
    up.solution.append("Up")
    if up.state not in visited_nodes_state:
      visited_nodes_state.append(up.state)
      expanded_nodes.append(up)

  if i_cord + 1 < 3:
    down = eight_puzzle()
    down.state = deepcopy(node.state)
    down.state[i_cord+1][j_cord], down.state[i_cord][j_cord] = down.state[i_cord][j_cord], down.state[i_cord+1][j_cord]
    down.g = node.g + 1
    down.h = calculate_h(down)
    down.solution = deepcopy(node.solution)
    down.solution.append("Down")
    if down.state not in visited_nodes_state:
      visited_nodes_state.append(down.state)
      expanded_nodes.append(down)
  return expanded_nodes
    
    
def queuing_func(nodes, expanded_nodes):
  global max_queue_size
  for item in expanded_nodes:
    heapq.heappush(nodes,item)
  if len(nodes) > max_queue_size:
    max_queue_size = len(nodes)
  return nodes

def general_search(problem):
  nodes = []
  nodes.append(problem)
  heapq.heapify(nodes)
  global max_queue_size 
  max_queue_size = len(nodes)
  visited_nodes_state.append(problem.state)
  while (1):
    if len(nodes) == 0:
      print ("Solution does not exist :(")
      exit()
    node = remove_front(nodes)
    if goal_test(node):
      return node
    nodes = queuing_func(nodes, expand(node))

problem = get_input()

goal = general_search(problem)
print ("Solution (Direction to move the blank tile):", goal.solution)
print ("Depth:", goal.g)
print("Maximum queue size: ", max_queue_size)
print("Total nodes expanded:", total_nodes_expanded)
