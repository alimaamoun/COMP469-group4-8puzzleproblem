import random
import math
import time

# Hill-Climb Algorithm
def hill_climb(n):
    #used to count the number of queens currently attacking each other on this board.
    #O(n^2) time complexity
    def conflicts(board):
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                #same row or same diagonal logic
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    count += 1
        return count

    #generates a random board where each queen is put into a random row in its column
    #means that columns are distinct, need to check for rows and diagonal only.
    def random_board(n):
        board = list(range(n))
        random.shuffle(board)
        return board

    #start with a random state and check its conflicts
    current = random_board(n)
    current_conflicts = conflicts(current)
    #loop generates all possible neighboring states
    #moves each queen in its column and looks for a better state
    #better means less conflicts in next_board
    while True:
        neighbors = []
        for i in range(n):
            for j in range(n):
                if j != current[i]:
                    neighbor = list(current)
                    neighbor[i] = j
                    neighbors.append(neighbor)
        next_board = min(neighbors, key=conflicts)
        next_conflicts = conflicts(next_board)
        if next_conflicts >= current_conflicts:
            break
        current, current_conflicts = next_board, next_conflicts
    return current, current_conflicts

# Simulated Annealing Algorithm
def simulated_annealing(n):
    #same conflicts function as before
    def conflicts(board):
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    count += 1
        return count

    #same method to get a random board
    def random_board(n):
        board = list(range(n))
        random.shuffle(board)
        return board

    #allowed temperature decreases over time
    #t is current iteration
    #decays over time
    def temperature(t):
        return max(0.1, 0.99 ** t)

    #probability of accepting a worse solution based on the temperature and change in # of conflicts
    def probability(delta_e, t):
        return math.exp(-delta_e / t)

    #start off with a random board and count its conflicts
    current = random_board(n)
    current_conflicts = conflicts(current)
    t = 1
    #MAIN LOOP
    while t < 10000:
        #generating a neighboring solution
        neighbor = list(current)
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]  # Swap rows
        #calculate the change in conflicts from current and neighbor state
        neighbor_conflicts = conflicts(neighbor)
        #calculate change in conflicts
        delta_e = neighbor_conflicts - current_conflicts
        #if the temperature is high enough, take the risk on the neighor with a worst cost.
        if delta_e < 0 or random.random() < probability(delta_e, temperature(t)):
            current, current_conflicts = neighbor, neighbor_conflicts
        #increase the time which will  lower the temperature
        t += 1
    return current, current_conflicts

# Genetic Algorithm
def genetic_algorithm(n, population_size=100, generations=1000, mutation_rate=0.01):
    #counts the number of conflicts in the board
    def conflicts(board):
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    count += 1
        return count

    #places a queen in a unique column.
    def random_board(n):
        board = list(range(n))
        random.shuffle(board)
        return board

    #combining two board states to make a new child board
    def crossover(parent1, parent2):
        n = len(parent1)
        child = [-1] * n  # Initialize child with placeholders (-1)

        # Choose two crossover points, will be used to copy from parent 1 into child
        start, end = sorted(random.sample(range(n), 2))

        # Copy the segment from parent1 to the child
        child[start:end + 1] = parent1[start:end + 1]

        # Fill the remaining positions with elements from parent2
        # making sure they are not already values in child. Ensures unique rows and columns
        for i in range(n):
            if parent2[i] not in child:
                for j in range(n):
                    if child[j] == -1:
                        child[j] = parent2[i]
                        break

        return child

    #randomly swap elements based on mutation rate.
    def mutate(board):
        if random.random() < mutation_rate:
            #select random values from board
            i, j = random.sample(range(n), 2)
            #swap them
            board[i], board[j] = board[j], board[i]  # Swap rows
        return board

    #start with the population of boards
    population = [random_board(n) for _ in range(population_size)]
    #each iteration is considered a generation
    for generation in range(generations):
        #sorts the population by number of conflicts to pick the best fit board
        population = sorted(population, key=conflicts)
        #if we find the lowest conflicting state has 0 conflicts, it is the goal state
        if conflicts(population[0]) == 0:
            break
        #start a new population from the top half
        #these will serve as parents for next generation
        #considered the more fitted individuals
        new_population = population[:population_size // 2]
        #generate new offspring
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:50], 2)
            child = mutate(crossover(parent1, parent2))
            new_population.append(child)
        population = new_population
    return population[0], conflicts(population[0])

# Performance Measurement
def measure_performance(algorithm, n, runs=10):
    times = []
    successes = 0
    for _ in range(runs):
        start_time = time.time()
        board, conflicts = algorithm(n)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        print(f"V number of conflicts: {conflicts}")
        print_board(board)
        if conflicts == 0:
            successes += 1
    return {
        'end result' : board,
        'algorithm': algorithm.__name__,
        'success_rate': successes / runs,
        'average_time': sum(times) / runs,
        'min_time': min(times),
        'max_time': max(times),
    }

def print_board(state):
    #state is a single dimensional array containing the row positions in each column index
    n = len(state)
    for column in range(n):
        for row in range(n):
            if state[column] == row:
                print('Q', end='  ')
            else:
                print('.', end='  ')
        print()


# Main Function
if __name__ == "__main__":
    n = 8
    runs = 10

    algorithms = [hill_climb, simulated_annealing, genetic_algorithm]
    results = []

    for algorithm in algorithms:
        result = measure_performance(algorithm, n, runs)
        results.append(result)
        print(f"End Result: {result["end result"]}")
        # print_board(result["end result"])
        print(f"Algorithm: {result['algorithm']}")
        print(f"Success Rate: {result['success_rate'] * 100}%")
        print(f"Average Time: {result['average_time']:.6f} seconds")
        print(f"Min Time: {result['min_time']:.6f} seconds")
        print(f"Max Time: {result['max_time']:.6f} seconds")
        print()

    # Comparison Summary
    print("Comparison Summary:")
    for result in results:
        print(result)