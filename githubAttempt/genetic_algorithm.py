import time
import random
import numpy as np

class MaxSatGeneticAlgorithm:
    def __init__(self, pop_size, tourn_size, mutation_rate, time_limit, max_sat_instance):
        self.pop_size = pop_size
        self.time_limit = time_limit
        self.tourn_size = tourn_size
        self.mutation_rate = mutation_rate
        self.max_sat_instance = max_sat_instance
        self.ind_size = max_sat_instance.num_vars

        self.start_time = 0
        self.current_pop = None
        self.current_pop_fitness = None

    def generate_initial_population(self):
        """Generate a random population of bitstrings."""
        self.current_pop = np.array([])
        self.current_pop_fitness = np.array([])
        max_num = 2 ** self.ind_size - 1

        for _ in range(self.pop_size):
            num = random.randint(0, max_num)
            bits = bin(num)[2:].zfill(self.ind_size)
            self.current_pop = np.append(self.current_pop, bits)
            self.current_pop_fitness = np.append(self.current_pop_fitness,
                                                 self.max_sat_instance.count_sat_clauses(bits))

    def tournament_selection(self):
        """Select a parent using tournament selection."""
        ind = np.random.randint(0, self.pop_size - 1, self.tourn_size)
        scores = self.current_pop_fitness[ind)

        winners = scores == max(scores)
        winner_pos = ind[winners][random.randint(0, len(scores[winners]) - 1)]
        return self.current_pop[winner_pos]

    def mutate(self, bits_x):
        """Mutate a bitstring by flipping bits with probability mutation_rate."""
        mutation_rate = self.mutation_rate / self.ind_size
        y = ''
        for bit in bits_x:
            prob = random.uniform(0, 1)
            y += self.bit_not(bit) if prob < mutation_rate else bit
        return y

    def uniform_crossover(self, bits_x, bits_y):
        """Combine two parents using uniform crossover."""
        child = ''
        for i in range(self.ind_size):
            child += bits_x[i] if random.uniform(0, 1) < 0.5 else bits_y[i]
        return child

    def run_ga(self):
        """Run the evolutionary algorithm."""
        t = 0
        fbest = 0
        xbest = ''
        fit = []
        generations = 0

        self.generate_initial_population()
        self.start_time = time.time()

        while True:
            fbest, xbest, second_best_fit, second_best_x = self.best_two_fit()

            # Stop if time budget is exceeded
            if time.time() - self.start_time > self.time_limit:
                break

            # Stop if all clauses are satisfied
            if fbest == self.max_sat_instance.num_clauses:
                break

            new_pop = np.array([])
            new_pop_fitness = np.array([])

            # Keep the best two individuals
            new_pop = np.append(new_pop, xbest)
            new_pop = np.append(new_pop, second_best_x)

            new_pop_fitness = np.append(new_pop_fitness, fbest)
            new_pop_fitness = np.append(new_pop_fitness, second_best_fit)

            # Generate new population
            while len(new_pop) < self.pop_size:
                x = self.tournament_selection()
                y = self.tournament_selection()

                # Create offspring using crossover and mutation
                new_individual = self.uniform_crossover(
                    self.mutate(x),
                    self.mutate(y)
                )

                new_pop = np.append(new_pop, new_individual)
                new_pop_fitness = np.append(new_pop_fitness, self.max_sat_instance.count_sat_clauses(new_individual))

            self.current_pop = new_pop
            self.current_pop_fitness = new_pop_fitness
            generations += 1
            fit.append(fbest)

        # Calculate runtime (number of generations × population size)
        t = generations * self.pop_size
        return t, fbest, xbest

    @staticmethod
    def bit_not(bit):
        """Flip a bit."""
        return '0' if bit == '1' else '1'