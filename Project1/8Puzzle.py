from copy import deepcopy
import heapq

class eight_puzzle:
  state = [[0,0,0],[0,0,0],[0,0,0]]
  g = -1
  h = -1
  def __lt__(self, other):
    return self.g + self.h < other.g + other.h

## 1)Uniform Cost Search
## TBD 2)A* with the Misplaced Tile heuristic
## TBD 3)A* with the Manhattan Distance heuristic
heuristic = 1

total_nodes_expanded = 0
visited_nodes_state = []

def calculate_h(node):
  if heuristic == 1:
    return 0
  
def get_input():
  problem = eight_puzzle()
  row1 = input("Enter first row (space separated):")
  problem.state[0] = [int(x) for x in row1.split()]
  row2 = input("Enter second row (space separated):")
  problem.state[1] = [int(x) for x in row2.split()]
  row3 = input("Enter third row (space separated):")
  problem.state[2] = [int(x) for x in row3.split()]
  problem.g = 1
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
    if left.state not in visited_nodes_state:
      visited_nodes_state.append(left.state)
      expanded_nodes.append(left)

  if j_cord + 1 < 3:
    right = eight_puzzle()
    right.state = deepcopy(node.state)
    right.state[i_cord][j_cord+1], right.state[i_cord][j_cord] = right.state[i_cord][j_cord], right.state[i_cord][j_cord+1]
    right.g = node.g + 1
    right.h = calculate_h(right)
    if right.state not in visited_nodes_state:
      visited_nodes_state.append(right.state)
      expanded_nodes.append(right)

  if i_cord - 1 > -1:
    up = eight_puzzle()
    up.state = deepcopy(node.state)
    up.state[i_cord-1][j_cord], up.state[i_cord][j_cord] = up.state[i_cord][j_cord], up.state[i_cord-1][j_cord]
    up.g = node.g + 1
    up.h = calculate_h(up)
    if up.state not in visited_nodes_state:
      visited_nodes_state.append(up.state)
      expanded_nodes.append(up)

  if i_cord + 1 < 3:
    down = eight_puzzle()
    down.state = deepcopy(node.state)
    down.state[i_cord+1][j_cord], down.state[i_cord][j_cord] = down.state[i_cord][j_cord], down.state[i_cord+1][j_cord]
    down.g = node.g + 1
    down.h = calculate_h(down)
    if down.state not in visited_nodes_state:
      visited_nodes_state.append(down.state)
      expanded_nodes.append(down)
  return expanded_nodes
    
    
def queuing_func(nodes, expanded_nodes):
  for item in expanded_nodes:
    heapq.heappush(nodes,item)
  return nodes

def general_search(problem):
  nodes = []
  nodes.append(problem)
  heapq.heapify(nodes)
  visited_nodes_state.append(problem.state)
  while (1):
    if len(nodes) == 0:
      return "Solution not found"
    node = remove_front(nodes)
    if goal_test(node):
      return "Success" + str(node.state)
    nodes = queuing_func(nodes, expand(node))

problem = get_input()
print(general_search(problem))
print("Total nodes expanded:", total_nodes_expanded)
