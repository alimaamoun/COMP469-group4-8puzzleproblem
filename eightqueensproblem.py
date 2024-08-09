import random
import math
import time

# Hill-Climb Algorithm
def hill_climb(n):
    def conflicts(board):
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    count += 1
        return count

    def random_board(n):
        return [random.randint(0, n - 1) for _ in range(n)]

    current = random_board(n)
    current_conflicts = conflicts(current)
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
    def conflicts(board):
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    count += 1
        return count

    def random_board(n):
        return [random.randint(0, n - 1) for _ in range(n)]

    def temperature(t):
        return max(0.1, 0.99 ** t)

    def probability(delta_e, t):
        return math.exp(-delta_e / t)

    current = random_board(n)
    current_conflicts = conflicts(current)
    t = 1
    while t < 10000:
        neighbor = list(current)
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        neighbor[i] = j
        #calculate the change in conflicts from current and neighbor state
        neighbor_conflicts = conflicts(neighbor)
        delta_e = neighbor_conflicts - current_conflicts
        if delta_e < 0 or random.random() < probability(delta_e, temperature(t)):
            current, current_conflicts = neighbor, neighbor_conflicts
        t += 1
    return current, current_conflicts

# Genetic Algorithm
def genetic_algorithm(n, population_size=100, generations=1000, mutation_rate=0.01):
    def conflicts(board):
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    count += 1
        return count

    def random_board(n):
        return [random.randint(0, n - 1) for _ in range(n)]

    def crossover(parent1, parent2):
        point = random.randint(0, n - 1)
        return parent1[:point] + parent2[point:]

    def mutate(board):
        if random.random() < mutation_rate:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            board[i] = j
        return board

    population = [random_board(n) for _ in range(population_size)]
    for generation in range(generations):
        population = sorted(population, key=conflicts)
        if conflicts(population[0]) == 0:
            break
        new_population = population[:population_size // 2]
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
        if conflicts == 0:
            successes += 1
    return {
        'algorithm': algorithm.__name__,
        'success_rate': successes / runs,
        'average_time': sum(times) / runs,
        'min_time': min(times),
        'max_time': max(times),
    }

# Main Function
if __name__ == "__main__":
    n = 8
    runs = 10

    algorithms = [hill_climb, simulated_annealing, genetic_algorithm]
    results = []

    for algorithm in algorithms:
        result = measure_performance(algorithm, n, runs)
        results.append(result)
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