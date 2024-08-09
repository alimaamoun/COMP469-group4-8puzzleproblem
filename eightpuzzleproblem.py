from collections import deque
import heapq
import time

class PuzzleState:
    def __init__(self, board, empty_tile, depth=0, parent=None):
        """Initializes the board of the 8-puzzle problem.


        Args:
            board (_type_): the boards current state
            empty_tile (_type_): The position of the empty tile '0'
            depth (int, optional): The current depth of the boards state Defaults to 0.
            parent (_type_, optional): _description_. Defaults to None.
        """
        self.board = board
        self.empty_tile = empty_tile
        self.depth = depth
        self.parent = parent

    def __lt__(self, other):
        return self.depth < other.depth

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))


    def get_neighbors(self):
        """get_neighbors() 
            Each direction is a node child of the current state. 
            This function pregenerates the possible paths one of the 
            future implemented search algorithms will take when trying 
            to solve this board.
            Generates the state space of the board.
        Returns:
            _type_: list of all neighbors of current board
        """
        #a list to store neighboring states
        neighbors = []
        #coordinates of empty tile
        x, y = self.empty_tile
        #possible actions to take
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        #iterating over each possible direction available above
        for dx, dy in directions:
            #nx,ny represent the new coordinates of the empty space after moving
            nx, ny = x + dx, y + dy
            #if the new location of the empty tile is in a valid position
            if 0 <= nx < 3 and 0 <= ny < 3:
                #new board initialiazation process
                new_board = [row[:] for row in self.board]
                #swap the location of the empty tile and the tile it moved to
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                #adds the new state to the list of neighbors and is linked to its parent state
                neighbors.append(PuzzleState(new_board, (nx, ny), self.depth + 1, self))
        #returns list of neighbors of the puzzle
        return neighbors

    def is_goal(self):
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def get_path(self):
        path = []
        state = self
        while state:
            path.append(state)
            state = state.parent
        return path[::-1]

def print_board(state):
    for row in state.board:
        print(row)
    print()

initial_board = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
initial_board2 = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
# MAX_ITERATION = 10000

empty_tile = (1, 1)
initial_state = PuzzleState(initial_board, empty_tile)
initial_state2 = PuzzleState(initial_board2, empty_tile)
print_board(initial_state)


###########################################################
###   BFS IMPLEMENTATION   ################################
###########################################################
def bfs(initial_state):
    """Breadth First Search Algoritm looks at all neighbors 
    of current depth level before moving on to the next

    Args:
        initial_state (_type_): Takes the intial state of the board as a parameter

    Returns:
        _type_: None
    """
    frontier = deque([initial_state])
    explored = set()
    iterations = 0
    while frontier and iterations <= MAX_ITERATION:
        state = frontier.popleft()
        #check if current state is equal to goal state
        if state.is_goal():
            #get all parents of goal state
            return state.get_path(), iterations
        #state was not goal state, add state to explored set
        explored.add(state)
        #move on to next neighbor in current depth
        for neighbor in state.get_neighbors():
            if neighbor not in explored and neighbor not in frontier:
                frontier.append(neighbor)
        iterations+=1
    return None, None

# print("BFS Solution:")
# start_time = time.time()
# path = bfs(initial_state)
# end_time = time.time()

# # for state in path:
# #     print_board(state)
# print(f"Time taken: {end_time - start_time} seconds")
# if(path):
#     print(f"Number of moves: {len(path) - 1}\n")
# else:
#     print(f"Failed to find solution in {MAX_ITERATION} iterations\n")


###########################################################
###   A* IMPLEMENTATION   #################################
###########################################################
def heuristic(state):
    """estimates the future cost of current state by looking at how far to the goal state 
    the current state is.
    g(n): depth from start to current node state
    h(n): future cost function from current state to goal state using manhattan distance

    Args:
        state (_type_): current state of the board

    Returns:
        _type_: estimated cost of the future path to goal
    """    
    #creates a dictionary of the goal state and the tile position 
    #to enable us to understand the costs of getting to the goal state
    goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1)}
    cost = 0
    #for each tile on the board (except empty tile) calculate the *manhattan distance* 
    #from its current position to its goal position
    for i in range(3):
        for j in range(3):
            #ignore the empty tile
            if state.board[i][j] != 0:
                #get the goal position for our current tile we are looking at
                goal_x, goal_y = goal_positions[state.board[i][j]]
                #manhattan distance function between goal state and current state; add to cost
                cost += abs(goal_x - i) + abs(goal_y - j)
    return cost

def astar(initial_state):
    """A* uses heuristics to guide itself towards the goal state
    uses a priority queue to look at the lowest costing path which is based on
    the heuristic() function.

    Args:
        initial_state (_type_): starting state of the puzzle board

    Returns:
        _type_: list of neighbors if a solution was found
    """    
    frontier = []
    #priority queue with items organized by priority (priority,state)
    #the priority is the result of the heuristic function on that state
    #add the initial state to the priority queue
    heapq.heappush(frontier, (heuristic(initial_state), initial_state))
    explored = set()
    iterations = 0
    while frontier and iterations <= MAX_ITERATION:
        #start with the state with the lowest cost
        _, state = heapq.heappop(frontier)
        #if state is the goal state, done; follow its parent states
        if state.is_goal():
            return state.get_path(), iterations
        #mark as visited
        explored.add(state)
        #add next neighbors to the priority queue if not already visited
        for neighbor in state.get_neighbors():
            if neighbor not in explored:
                heapq.heappush(frontier, (neighbor.depth + heuristic(neighbor), neighbor))
        iterations += 1
    return None, None

# print("A* Solution:")
# start_time = time.time()
# path = astar(initial_state)
# end_time = time.time()

# # for state in path:
# #     print_board(state)
# print(f"Time taken: {end_time - start_time} seconds")
# if(path):
#     print(f"Number of moves: {len(path) - 1}\n")
# else:
#     print(f"Failed to find solution in {MAX_ITERATION} iterations\n")



###########################################################
###   DFS IMPLEMENTATION   ################################
###########################################################

def dfs(initial_state):
    """
        Depth First Search algorithm takes each board configuration possibly and checks by depth
        This algorithm will do this until a solution is found if possible

    Args:
        initial_state (_type_): Takes the intial state of the board as a parameter

    Returns:
        _type_: None
    """    
    frontier = [initial_state]
    explored = set()   # creates a set of paths to not be repeated
    iterations = 0
    while frontier and iterations <= MAX_ITERATION:
        state = frontier.pop()
        # print_board(state)
        if state.is_goal(): # Checks to see if current state == goal state, if yes then it returns and gets path, if no then keep running
            return state.get_path(), iterations
        explored.add(state) # adds current state to the set to not be repeated
        for neighbor in state.get_neighbors():
            if neighbor not in explored and neighbor not in frontier: # Grabs the next state that has not been visisted or explored
                frontier.append(neighbor)
        iterations += 1
    return None, None

# print("DFS Solution:")
# start_time = time.time()
# path = dfs(initial_state)
# end_time = time.time()

# # for state in path:
# #     print_board(state)
# print(f"Time taken: {end_time - start_time} seconds")
# if(path):
#     print(f"Number of moves: {len(path) - 1}\n")
# else:
#     print(f"Failed to find solution in {MAX_ITERATION} iterations\n")


###########################################################
###   GREEDY BEST-FIRST SEARCH IMPLEMENTATION   ###########
###########################################################

# ********** THIS ALSO USES THE HUERISTIC FUNCTION IN A* ALGORITHM *********

def greedy_best_first(initial_state):
    """
       This uses the Hueristic function to calculate the least cost effective path and 
       will take it even if the next path is not towards the solution

    Args:
        initial_state (_type_): Takes the intial state of the board as a parameter

    Returns:
        _type_: None
    """    
    frontier = []
    heapq.heappush(frontier, (heuristic(initial_state), initial_state))
    explored = set()
    iterations = 0
    while frontier and iterations <= MAX_ITERATION:
        _, state = heapq.heappop(frontier) # unpacks and pops the heapq's smallest element and stores that value into 'state'
        if state.is_goal(): # if the current state matches the goal state then the algorithm finishes and returns the complete path to the solution
            return state.get_path(), iterations
        explored.add(state) # adds current state to the set to not be repeated
        for neighbor in state.get_neighbors():
            if neighbor not in explored:
                heapq.heappush(frontier, (heuristic(neighbor), neighbor)) # Grabs the next state that has not been visisted or explored
        iterations += 1
    return None, None

# print("Greedy Best-First Solution:")
# start_time = time.time()
# path = greedy_best_first(initial_state)
# end_time = time.time()
# # for state in path:
# #     print_board(state)
# print(f"Time taken: {end_time - start_time} seconds")
# if(path):
#     print(f"Number of moves: {len(path) - 1}\n")
# else:
#     print(f"Failed to find solution in {MAX_ITERATION} iterations\n")


###########################################################
###   IDS IMPLEMENTATION   ################################
###########################################################

# def ids(initial_state):
#     """ Iterative Depth Search
#     This will run the inner dfs_limited(state, depth_limit) function and will increase depth tentatively until the solution is found.

#     Args:
#         initial_state (_type_): Takes the intial state of the board as a parameter
#     """    
#     def dfs_limited(state, depth_limit, iteration=0):
#         """ Works with the ids(initial_state) function.  This function checks to see if the goal state is reached, 
#         if the depth limit is reached, then goes to the next neighbor with the depth limit decreased.

#         Args:
#             state (_type_): Current board state
#             depth_limit (_type_): How deep the depth can go

#         Returns:
#             _type_: None
#         """        
#         maxiteration = 50
#         iteration += 1
#         current_time = time.time()
#         if(current_time - start_time > 10):
#             return None, None
#         if state.is_goal(): # checks to see if the goal state is reached
#             return state.get_path()
#         if depth_limit == 0 or iteration >= MAX_ITERATION: # checks to see if the depth limit is 0
#             return None, None
#         for neighbor in state.get_neighbors(): # gets the next neighbor
#             result = dfs_limited(neighbor, depth_limit - 1, iteration) #recurses next state with a lower depth limit
#             if result:
#                 return result
#         return None, None

#     depth = 0
#     iterations = 0
#     while iterations <= MAX_ITERATION : # runs the inner function until solution is found
#         result = dfs_limited(initial_state, depth, iterations)
#         iterations += 1
#         if result:
#             return result, iterations
#         depth += 1

# def ids(initial_state, max_depth=50):
#     """ Iterative Depth Search
#     This will run the inner dfs_limited(state, depth_limit) function and will increase depth tentatively until the solution is found.

#     Args:
#         initial_state (_type_): Takes the intial state of the board as a parameter
#     """    
#     def dfs_limited(state, depth_limit, iterations):
#         """ Works with the ids(initial_state) function.  This function checks to see if the goal state is reached, 
#         if the depth limit is reached, then goes to the next neighbor with the depth limit decreased.

#         Args:
#             state (_type_): Current board state
#             depth_limit (_type_): How deep the depth can go

#         Returns:
#             _type_: None
#         """
#         #initialize stack of state and depth limit
#         stack = [(state, 0)]
#         #initialize explored states
#         explored = set()
#         # while we have more states in the stack and have not passed limitations
#         while stack and iterations[0] < MAX_ITERATION:
#             #current state of board
#             current_state, depth = stack.pop()
#             #if current state is equal to goal state
#             if current_state.is_goal():
#                 return current_state.get_path(), iterations[0]
#             #depth limit for simplicity
#             if depth < depth_limit:
#                 #mark as visited
#                 explored.add(current_state)
#                 #prepare next iteration
#                 for neighbor in current_state.get_neighbors():
#                     if neighbor not in explored:
#                         stack.append((neighbor, depth + 1))
#             iterations[0] += 1
#         return None, None

#     iterations = [0]
#     for depth in range(max_depth):
#         #start recursive steps
        
#         result, iterations[0] = dfs_limited(initial_state, depth, iterations)
#         print(f"iterations: {iterations[0]}\n")
#         if result:
#             return result, iterations[0]
#         if iterations[0] >= MAX_ITERATION:
#             break
#     return None, None

def ids(initial_state, max_depth=50):
    def dfs_limited(state, depth_limit, iterations):
        stack = [(state, 0)]
        while stack and iterations[0] < MAX_ITERATION:
            current_state, depth = stack.pop()
            if current_state.is_goal():
                return current_state.get_path(), iterations[0]
            if depth < depth_limit:
                stack.extend((neighbor, depth + 1) for neighbor in reversed(current_state.get_neighbors()))
            iterations[0] += 1
        return None, None

    iterations = [0]
    for depth in range(max_depth):
        result, total_iterations = dfs_limited(initial_state, depth, iterations)
        if result:
            return result, total_iterations
        if iterations[0] >= MAX_ITERATION:
            break
    return None, None



# print("IDS Solution:")
# start_time = time.time()
# path = ids(initial_state)
# end_time = time.time()
# # for state in path:
# #     print_board(state)
# print(f"Time taken: {end_time - start_time} seconds")
# if(path):
#     print(f"Number of moves: {len(path) - 1}\n")
# else:
#     print(f"Failed to find solution in {MAX_ITERATION} iterations\n")

MAX_ITERATION = 10000

initial_boards = [
    [[1, 2, 3], [4, 5, 6], [7, 0, 8]],  # Test Case 1
    [[1, 2, 3], [4, 5, 6], [0, 7, 8]],  # Test Case 2
    [[1, 2, 3], [5, 0, 6], [4, 7, 8]],  # Test Case 3
    [[1, 2, 3], [5, 6, 0], [4, 7, 8]],  # Test Case 4
    [[1, 2, 3], [4, 0, 5], [7, 8, 6]],  # Test Case 5
    [[2, 8, 3], [1, 6, 4], [7, 0, 5]],  # Test Case 6
    [[2, 1, 6], [4, 0, 8], [7, 5, 3]],  # Test Case 7
    [[5, 6, 7], [4, 0, 8], [3, 2, 1]],  # Test Case 8
    [[1, 2, 0], [4, 5, 3], [7, 8, 6]],  # Test Case 9
    [[8, 6, 7], [2, 5, 4], [3, 0, 1]]   # Test Case 10
]



for board in initial_boards:
    empty_tile = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0][0]
    initial_state = PuzzleState(board, empty_tile)
    print("Testing board:")
    print_board(initial_state)

    #run BFS
    print("BFS Solution:")
    start_time = time.time()
    path, iterations = bfs(initial_state)
    end_time = time.time()

    # for state in path:
    #     print_board(state)
    print(f"Time taken: {end_time - start_time} seconds")
    if(path):
        print(f"Number of moves: {len(path) - 1}")
        print(f"Number of iterations: {iterations}\n")
    else:
        print(f"Failed to find solution in {MAX_ITERATION} iterations\n")

    
    
    #RUN DFS
    print("DFS Solution:")
    start_time = time.time()
    path, iterations = dfs(initial_state)
    end_time = time.time()
    # for state in path:
    #     print_board(state)
    print(f"Time taken: {end_time - start_time} seconds")
    if(path):
        print(f"Number of moves: {len(path) - 1}")
        print(f"Number of iterations: {iterations}\n")
    else:
        print(f"Failed to find solution in {MAX_ITERATION} iterations\n")
    
    
    #RUN A*
    print("A* Solution:")
    start_time = time.time()
    path, iterations = astar(initial_state)
    end_time = time.time()
    # for state in path:
    #     print_board(state)
    print(f"Time taken: {end_time - start_time} seconds")
    if(path):
        print(f"Number of moves: {len(path) - 1}")
        print(f"Number of iterations: {iterations}\n")
    else:
        print(f"Failed to find solution in {MAX_ITERATION} iterations\n")
    
    
    #RUN GFS
    print("Greedy Best-First Solution:")
    start_time = time.time()
    path, iterations = greedy_best_first(initial_state)
    end_time = time.time()
    # for state in path:
    #     print_board(state)
    print(f"Time taken: {end_time - start_time} seconds")
    if(path):
        print(f"Number of moves: {len(path) - 1}")
        print(f"Number of iterations: {iterations}\n")
    else:
        print(f"Failed to find solution in {MAX_ITERATION} iterations\n")
    
    
    #RUN IDS
    print("IDS Solution:")
    start_time = time.time()
    path, iterations = ids(initial_state, max_depth=100)
    end_time = time.time()
    # for state in path:
    #     print_board(state)
    print(f"Time taken: {end_time - start_time} seconds")
    if(path):
        print(f"Number of moves: {len(path) - 1}")
        print(f"Number of iterations: {iterations}\n")
    else:
        print(f"Failed to find solution in {MAX_ITERATION} iterations\n")