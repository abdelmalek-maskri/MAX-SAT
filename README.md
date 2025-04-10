# MAXSAT Solver using Evolutionary Algorithm

This project provides a Python-based solver for the MAXSAT problem using a basic **evolutionary algorithm**. It is designed to work with **weighted DIMACS (WDIMACS)** files and allows clause satisfaction analysis, fitness evaluation, and evolutionary search for optimal or near-optimal solutions.

## 📁 Project Structure

```
.
├── maxsat_solver.py     # Main solver and experiment runner
├── Dockerfile           # Optional Docker setup
├── README.md            # This file
└── test_files/          # Folder for input .wdimacs test files
```

## ✅ Features

- Parses `.wdimacs` files and evaluates clause satisfaction.
- Supports command-line operations for:
  - Clause checking
  - Clause counting
  - Evolutionary optimization
- Optional experiment runner with parameter sweep
- Optional data visualization with Seaborn (commented in by default)

---

## 🔧 Setup

### Dependencies
Install these Python libraries if running experiments or plots:
```bash
pip install pandas seaborn matplotlib
```

### Make executable (optional)
```bash
chmod +x maxsat_solver.py
```

---

## 🚀 Usage

### Question 1: Check if a single clause is satisfied

```bash
python3 maxsat_solver.py -question 1 -clause "w 1 -3 0" -assignment 101
```

### Question 2: Count satisfied clauses from a `.wdimacs` file

```bash
python3 maxsat_solver.py -question 2 -wdimacs test_files/example.wdimacs -assignment 10101
```

### Question 3: Run the evolutionary MAXSAT solver

```bash
python3 maxsat_solver.py -question 3 -wdimacs test_files/example.wdimacs -time_budget 10 -repetitions 3
```

This will output:
```
<evaluations>   <satisfied_clauses>   <best_assignment>
```

---

## ⚙️ Evolutionary Algorithm Details

- **Selection**: Tournament
- **Crossover**: Single-point (default) – adaptive and uniform versions available
- **Mutation**: Bit-flip mutation
- **Fitness Function**: Number of clauses satisfied

You can enable additional selection and variation strategies by uncommenting the corresponding sections in the script.

---

## 📊 Experiments & Plots (Optional)

Uncomment the following in `maxsat_solver.py` to run large-scale experiments:
```python
# df_results = run_experiments(clauses, num_vars)
# generate_boxplots(df_results)
```

This will:
- Run multiple configurations of the algorithm
- Save results as a CSV
- Generate boxplots to visualize performance of each parameter


