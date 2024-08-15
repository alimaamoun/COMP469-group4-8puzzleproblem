import math
import time  # Import time module to measure performance

# Constants for players
HUMAN = -1  # 'O' in this example
COMP = 1    # 'X' in this example

# Global variables to track performance
nodes_explored = 0
max_depth_reached = 0
total_time_spent = 0.0  # To accumulate the total time spent in AI decision-making

# Function to print the Tic Tac Toe board
def print_board(state):
    chars = {0: ' ', HUMAN: 'O', COMP: 'X'}
    for row in range(3):
        print(f'{chars[state[row*3]]} | {chars[state[row*3+1]]} | {chars[state[row*3+2]]}')
        if row < 2:
            print('--+---+--')
    print()

# Simplified function to check for a win
def evaluate(state):
    # Check rows
    for i in range(0, 9, 3):
        if state[i] == state[i + 1] == state[i + 2] and state[i] != 0:
            return state[i]

    # Check columns
    for i in range(3):
        if state[i] == state[i + 3] == state[i + 6] and state[i] != 0:
            return state[i]

    # Check diagonals
    if state[0] == state[4] == state[8] and state[0] != 0:
        return state[0]
    if state[2] == state[4] == state[6] and state[2] != 0:
        return state[2]

    # If no winner, return 0
    return 0

# Function to check if the board is full (i.e., no more moves)
def is_full(state):
    return 0 not in state

# Minimax function with alpha-beta pruning and debug information
def minimax(state, depth, player):
    global nodes_explored, max_depth_reached
    nodes_explored += 1
    max_depth_reached = max(max_depth_reached, depth)

    score = evaluate(state)

    # If COMP wins
    if score == COMP:
        return score

    # If HUMAN wins
    if score == HUMAN:
        return score

    # If it's a draw
    if is_full(state):
        return 0

    if player == COMP:
        max_eval = -math.inf
        for i in range(9):
            if state[i] == 0:
                state[i] = COMP
                eval = minimax(state, depth + 1, HUMAN)
                state[i] = 0
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if state[i] == 0:
                state[i] = HUMAN
                eval = minimax(state, depth + 1, COMP)
                state[i] = 0
                min_eval = min(min_eval, eval)
        return min_eval

# Function to get the best move for the AI (COMP) with debug information and time tracking
def best_move(state):
    global total_time_spent
    best_value = -math.inf
    move = -1
    print("AI is evaluating possible moves...")
    
    # Start time measurement
    start_time = time.time()
    
    for i in range(9):
        if state[i] == 0:
            state[i] = COMP
            move_value = minimax(state, 0, HUMAN)
            state[i] = 0
            print(f"Move {i + 1} -> Evaluated score: {move_value}")
            if move_value > best_value:
                best_value = move_value
                move = i
    
    # End time measurement
    end_time = time.time()
    
    # Calculate time spent and accumulate it
    time_spent = end_time - start_time
    total_time_spent += time_spent
    print(f"AI selects move {move + 1} with score {best_value} (Time spent: {time_spent:.4f} seconds)")
    return move

# Main function to play the game with performance output
def play_game():
    global nodes_explored, max_depth_reached, total_time_spent
    state = [0] * 9  # Initial empty board
    print_board(state)

    while True:
        # Human move
        human_move = int(input("Enter your move (1-9): ")) - 1
        if state[human_move] != 0:
            print("Invalid move! Try again.")
            continue
        state[human_move] = HUMAN

        print_board(state)

        if evaluate(state) == HUMAN:
            print("You win!")
            break
        if is_full(state):
            print("It's a draw!")
            break

        # Reset performance tracking for the current move
        nodes_explored = 0
        max_depth_reached = 0

        # AI move
        ai_move = best_move(state)
        state[ai_move] = COMP
        print_board(state)

        if evaluate(state) == COMP:
            print("AI wins!")
            break
        if is_full(state):
            print("It's a draw!")
            break

        # Output performance data
        print(f"Nodes explored: {nodes_explored}")
        print(f"Max depth reached: {max_depth_reached}")
        print(f"Total time spent by AI so far: {total_time_spent:.4f} seconds")

# Run the game
play_game()
