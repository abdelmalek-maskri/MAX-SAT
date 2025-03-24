#!/usr/bin/env python3
import sys
import random
import time
#Uncomment this if you want to run the experiment 

# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

#Exo1
#determines if a given clause is satisfied by a variable assignment.
def is_clause_satisfied(clause: str, assignment: str) -> int:
    #split the clause and ignore the first and last elements
    parts = clause.split()
    if len(parts) > 2:
        literals = parts[1:-1]
    else:
        literals = []

    #convert the remaining parts to integers
    literals = [int(literal) for literal in literals]

    num_vars = len(assignment)  #Number of variables

    for literal in literals:
        var_index = abs(literal) - 1  #convert to zero-based index
        if var_index < num_vars:
            var_value = int(assignment[var_index])
            #check if clause is satisfied
            if (literal > 0 and var_value == 1) or (literal < 0 and var_value == 0):
                return 1  
    return 0 


#Exo2
#reads a WDIMACS file and counts the number of satisfied clauses for a given assignment.
def count_satisfied_clauses(wdimacs_file: str, assignment: str) -> int:
    total_clauses = 0
    satisfied_count = 0
    
    with open(wdimacs_file, 'r') as file:
        for line in file:
            if line.startswith('c') or line.startswith('p'):
                continue  #ignore comments and problem definition
            
            total_clauses += 1
            #evaluate whether the clause is satisfied by the assignment
            if is_clause_satisfied(line.strip(), assignment):
                satisfied_count += 1
    
    return satisfied_count


#Exo3
def parse_wdimacs_file(wdimacs_file: str):
    #parses a wdimacs file
    num_vars = 0
    num_clauses = 0
    clauses = []
    
    try:
        with open(wdimacs_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  #skip empty lines
                if line.startswith('c'):
                    continue  #ignore comments
                if line.startswith('p'):
                    #expected format: p <format> <num_vars> <num_clauses>
                    parts = line.split()
                    if len(parts) >= 4:
                        num_vars = int(parts[2])
                        num_clauses = int(parts[3])
                    else:
                        raise ValueError("Problem line does not contain enough information.")
                    continue
                #process clause lines:
                parts = line.split()
                if len(parts) < 2:
                    continue
                #ignore the first element and the trailing 0.
                clause_literals = [int(x) for x in parts[1:-1]]
                clauses.append(clause_literals)
    except FileNotFoundError:
        print(f"Error: WDIMACS file '{wdimacs_file}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    return num_vars, num_clauses, clauses

def count_satisfied_clauses_from_parsed(assignment: str, clauses: list) -> int:
    
    #evaluates the fitness (number of satisfied clauses) of an assignment using pre-parsed clauses.
    satisfied_count = 0

    #convert the assignment string into a list of integers for indexing.
    assignment_list = [int(bit) for bit in assignment]
    for clause in clauses:
        for literal in clause:
            var_index = abs(literal) - 1  #adjust for 0-based index.
            if (literal > 0 and assignment_list[var_index] == 1) or \
               (literal < 0 and assignment_list[var_index] == 0):
                satisfied_count += 1
                break  #stop after the first satisfying literal.
    return satisfied_count


def initialize_population(population_size, num_vars):
    #create random bitstrings for initial population
    return [[random.randint(0, 1) for _ in range(num_vars)] for _ in range(population_size)]

def tournamen_selection(population, fitness_values, tournament_size):
    #select individuals for breeding (tournament selection example)
    selected = []
    for _ in range(len(population)):
        #select random individuals for tournament
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitness = [fitness_values[i] for i in tournament_indices]
        
        #select the winner (highest fitness)
        winner_idx = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        selected.append(population[winner_idx])
    
    return selected

def crossover(parent1, parent2):
    #perform crossover between two parents
    if len(parent1) <= 1:
        return parent1[:], parent2[:]
        
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutate(individual, mutation_rate):

    mutated = individual[:]
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = 1 - mutated[i]  
    return mutated

def evolutionary_algorithm_for_maxsat(time_budget, num_vars, clauses, population_size, mutation_rate, crossover_rate, tournament_size):
    
    #initialize population randomly
    population = initialize_population(population_size, num_vars)
    
    evaluations = 0
    generations = 0
    best_fitness = 0
    best_solution = None
    evolution_logs = []  #list to store log entries

    
    start_time = time.time()
    while time.time() - start_time < time_budget:
        generations += 1
        #evaluate fitness of each individual
        fitness_values = [
            count_satisfied_clauses_from_parsed(''.join(map(str, individual)), clauses)
            for individual in population
        ]
        evaluations += population_size

        current_best = max(fitness_values)
        current_avg = sum(fitness_values) / len(fitness_values)

        #append current metrics to the log.
        evolution_logs.append({
            'generation': generations,
            'evaluations': evaluations,
            'best_fitness': current_best,
            'avg_fitness': current_avg
        })
        
        #track best solution
        current_best_idx = fitness_values.index(max(fitness_values))
        if fitness_values[current_best_idx] > best_fitness:
            best_fitness = fitness_values[current_best_idx]
            best_solution = population[current_best_idx]
        
        selected = tournamen_selection(population, fitness_values, tournament_size)
        
        new_population = []
        while len(new_population) < population_size:
            parent1 = selected[random.randint(0, len(selected) - 1)]
            parent2 = selected[random.randint(0, len(selected) - 1)]
            
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
                # child1, child2 = uniform_crossover(parent1, parent2)
                # child1, child2 = adaptive_crossover(parent1, parent2, crossover_rate, generations, 100)

            else:
                child1, child2 = parent1[:], parent2[:]

            # child1 = adaptive_mutate(child1, mutation_rate, generations, 100)
            # child2 = adaptive_mutate(child2, mutation_rate, generations, 100)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            
            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)
        
        population = new_population
    
    #print evolution log after the algorithm finishes.
    #uncomment this to see a detailed output
    
    # print_evolution_log(evolution_logs)

    xbest = ''.join(map(str, best_solution))
    t = generations * evaluations
    return t, best_fitness, xbest

def print_evolution_log(logs):
    #prints the evolution log stored in a list of dictionaries.
    #each log entry should have 'generation', 'evaluations', 'best_fitness', and 'avg_fitness' keys.

    print("Generation\tEvaluations\tBest_Fitness\tAvg_Fitness")
    for log in logs:
        print(f"{log['generation']}\t\t{log['evaluations']}\t\t{log['best_fitness']}\t\t{log['avg_fitness']:.2f}")


# def rank_selection(population, fitness_values):
#     sorted_population = [x for _, x in sorted(zip(fitness_values, population), reverse=True)]
#     probabilities = [(i+1) / sum(range(1, len(sorted_population) + 1)) for i in range(len(sorted_population))]

#     selected = []
#     for _ in range(len(population)):
#         selected.append(random.choices(sorted_population, probabilities)[0])

#     return selected

# def uniform_crossover(parent1, parent2, crossover_rate=0.85):
#     if random.random() > crossover_rate:
#         return parent1[:], parent2[:]
    
#     child1, child2 = parent1[:], parent2[:]
#     for i in range(len(parent1)):
#         if random.random() < 0.5:
#             child1[i], child2[i] = child2[i], child1[i]  #swap genes randomly
#     return child1, child2

# def adaptive_crossover(parent1, parent2, initial_crossover_rate, generation, max_generations):
#     adaptive_rate = initial_crossover_rate * (1 - generation / max_generations)
#     if random.random() < adaptive_rate:
#         return crossover(parent1, parent2)
#     else:
#         return parent1[:], parent2[:]

# def adaptive_mutate(individual, mutation_rate, generation, max_generations):
#     adaptive_rate = mutation_rate * (1 - (generation / max_generations))  #decrease over time
#     mutated = individual[:]
#     for i in range(len(mutated)):
#         if random.random() < adaptive_rate:
#             mutated[i] = 1 - mutated[i]  
#     return mutated


# ------------------------------
# Experiment Runner
# ------------------------------

def run_experiments(clauses, num_vars, time_budget=10, repetitions=100):
    #runs experiments by varying population size, mutation rate, and crossover rate
    results = []

    pop_sizes = [20, 50, 100, 200]
    # pop_sizes = [30, 20]
    # mutation_rates = [0.01, 0.05, 0.1]
    mutation_rates = [0.05]
    # crossover_rates = [0.6, 0.85, 1.0]
    crossover_rates = [0.85]

    for pop_size in pop_sizes:
        print(f"pop size: {pop_size}")
        for mutation_rate in mutation_rates:
            print(f"mutation rate:  {mutation_rate}")
            for crossover_rate in crossover_rates:
                print(f"crossover rate:  {crossover_rate}")
                for _ in range(repetitions):
                    t, nsat, _ = evolutionary_algorithm_for_maxsat(time_budget, num_vars, clauses, pop_size, mutation_rate, crossover_rate, tournament_size)
                    results.append({
                        "Population Size": pop_size,
                        "Mutation Rate": mutation_rate,
                        "Crossover Rate": crossover_rate,
                        "Satisfied Clauses": nsat
                    })

    df = pd.DataFrame(results)
    df.to_csv("experiment_results_normalized-f2000.wcnf.csv", index=False)  # Save results
    # df.to_csv("pop.csv", index=False)  # Save results
    return df

# ------------------------------
# Boxplot Generator
# ------------------------------

def generate_boxplots(df):
    #generates boxplots for parameter analysis
    
    # df = pd.read_csv(csv_file)

    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Population Size", y="Satisfied Clauses", data=df)
    plt.title("Impact of Population Size on Solution Quality")
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Mutation Rate", y="Satisfied Clauses", data=df)
    plt.title("Impact of Mutation Rate on Solution Quality")
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Crossover Rate", y="Satisfied Clauses", data=df)
    plt.title("Impact of Crossover Rate on Solution Quality")
    plt.show()


if __name__ == "__main__":
    #CLI interface to handle command-line inputs
    args = sys.argv

    if "-question" in args:
        question = args[args.index("-question") + 1]

        if question == "1":
            #clause Checking
            if "-clause" in args and "-assignment" in args:
                clause = args[args.index("-clause") + 1]
                assignment = args[args.index("-assignment") + 1]
                result = is_clause_satisfied(clause, assignment)
                print(result)
            else:
                print("Error: Missing -clause or -assignment argument for question 1.")
                sys.exit(1)

        elif question == "2":
            #WDIMACS Clause Counting
            if "-wdimacs" in args and "-assignment" in args:
                wdimacs_file = args[args.index("-wdimacs") + 1]
                assignment = args[args.index("-assignment") + 1]
                result = count_satisfied_clauses(wdimacs_file, assignment)
                print(result)
            else:
                print("Error: Missing -wdimacs or -assignment argument for question 2.")
                sys.exit(1)

        elif question == "3":
            #evolutionary Algorithm for MAXSAT
            if "-wdimacs" in args and "-time_budget" in args and "-repetitions" in args:
                wdimacs_file = args[args.index("-wdimacs") + 1]
                try:
                    time_budget = float(args[args.index("-time_budget") + 1])
                    if time_budget <= 0:
                        raise ValueError("Time budget must be a positive number.")
                except ValueError:
                    print("Error: Invalid time budget. Must be a positive number.")
                    sys.exit(1)

                try:
                    repetitions = int(args[args.index("-repetitions") + 1])
                    if repetitions <= 0:
                        raise ValueError("Repetitions must be a positive integer.")
                except ValueError:
                    print("Error: Invalid repetitions. Must be a positive integer.")
                    sys.exit(1)
                
                num_vars, num_clauses, clauses = parse_wdimacs_file(wdimacs_file)
                population_size = 20
                mutation_rate = 0.05
                crossover_rate = 0.85
                tournament_size = 5
                for _ in range(repetitions):
                    t, nsat, xbest = evolutionary_algorithm_for_maxsat(time_budget, num_vars, clauses, population_size, mutation_rate, crossover_rate, tournament_size)
                    print(f"{t}\t{nsat}\t{xbest}")
                
                #Uncomment this to run the experiments 

                # print("Running experiments... (this will take some time)")
                # df_results = run_experiments(clauses, num_vars)

                # print("Generating boxplots...")
                
                # generate_boxplots("experiment_results_wb-debug.dimacs.wcnf(large).csv")
                # generate_boxplots(df_results)

                # print("Results saved in 'experiment_results.csv'.")
                
            else:
                print("Error: Missing -wdimacs, -time_budget, or -repetitions argument for question 3.")
                sys.exit(1)

        else:
            print("Error: Invalid question number. Use 1, 2, or 3.")
            sys.exit(1)

    else:
        print("Error: Missing -question argument.")
        sys.exit(1)
