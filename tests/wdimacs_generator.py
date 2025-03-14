#!/usr/bin/env python3
"""
WDIMACS Test Files Generator
Creates various WDIMACS files for testing the MAXSAT solver

This script generates several WDIMACS files with different complexity levels
for thorough testing of your MAXSAT solver implementation.
"""

import os

# Create a directory for the test files
if not os.path.exists('test_files'):
    os.makedirs('test_files')

# Test File 1: Simple example from the assignment
with open('test_files/example1.wcnf', 'w') as f:
    f.write("""c Example file from assignment
p wcnf 4 2
0 1 2 3 4 0
0 -1 -2 3 -4 0
""")

# Test File 2: Assignment example from page 2
with open('test_files/example2.wcnf', 'w') as f:
    f.write("""c Example from assignment page 2
p wcnf 3 2
0 -1 2 3 0
0 1 2 3 0
""")

# Test File 3: More complex example with 10 variables and 8 clauses
with open('test_files/complex.wcnf', 'w') as f:
    f.write("""c Complex WDIMACS file
p wcnf 10 8
c This is a comment line
0 1 2 3 0
0 -1 -2 -3 0
0 4 5 -6 0
0 -4 -5 6 0
0 7 -8 9 -10 0
0 -7 8 -9 10 0
0 1 -3 5 -7 9 0
0 -2 4 -6 8 -10 0
""")

# Test File 4: Edge cases with empty clauses and many comments
with open('test_files/edge_cases.wcnf', 'w') as f:
    f.write("""c File with edge cases
c Multiple comment lines
c should be ignored
p wcnf 5 4
c Comment between clauses
0 1 2 3 0
0 0
c Another comment
0 -4 5 0
0 -1 -2 -3 -4 -5 0
""")

# Test File 5: Large variable indices
with open('test_files/large_indices.wcnf', 'w') as f:
    f.write("""c File with large variable indices
p wcnf 100 3
0 10 20 30 40 50 0
0 -25 -50 -75 -100 0
0 1 -10 20 -30 40 -50 60 -70 80 -90 100 0
""")

# Test File 6: All positive literals
with open('test_files/all_positive.wcnf', 'w') as f:
    f.write("""c File with all positive literals
p wcnf 5 3
0 1 2 3 4 5 0
0 1 3 5 0
0 2 4 0
""")

# Test File 7: All negative literals
with open('test_files/all_negative.wcnf', 'w') as f:
    f.write("""c File with all negative literals
p wcnf 5 3
0 -1 -2 -3 -4 -5 0
0 -1 -3 -5 0
0 -2 -4 0
""")

# Test File 8: Mixed literals with known satisfiability patterns
with open('test_files/known_patterns.wcnf', 'w') as f:
    f.write("""c File with known satisfiability patterns
p wcnf 5 5
c Always satisfiable (tautology: x1 OR NOT x1)
0 1 -1 0
c Satisfiable only when x1=1
0 1 0
c Satisfiable only when x1=0
0 -1 0
c Satisfiable when any of x2, x3, x4 is 1
0 2 3 4 0
c Satisfiable when all of x3, x4, x5 are 0
0 -3 -4 -5 0
""")

# Test File 9: A more realistic SAT problem
with open('test_files/realistic.wcnf', 'w') as f:
    f.write("""c A 3-SAT problem with 20 variables and 50 clauses
p wcnf 20 50
0 1 2 3 0
0 -1 -2 3 0
0 1 -3 4 0
0 -1 3 -4 0
0 2 -4 5 0
0 -2 4 -5 0
0 3 -5 6 0
0 -3 5 -6 0
0 4 -6 7 0
0 -4 6 -7 0
0 5 -7 8 0
0 -5 7 -8 0
0 6 -8 9 0
0 -6 8 -9 0
0 7 -9 10 0
0 -7 9 -10 0
0 8 -10 11 0
0 -8 10 -11 0
0 9 -11 12 0
0 -9 11 -12 0
0 10 -12 13 0
0 -10 12 -13 0
0 11 -13 14 0
0 -11 13 -14 0
0 12 -14 15 0
0 -12 14 -15 0
0 13 -15 16 0
0 -13 15 -16 0
0 14 -16 17 0
0 -14 16 -17 0
0 15 -17 18 0
0 -15 17 -18 0
0 16 -18 19 0
0 -16 18 -19 0
0 17 -19 20 0
0 -17 19 -20 0
0 18 -20 1 0
0 -18 20 -1 0
0 19 -1 2 0
0 -19 1 -2 0
0 20 -2 3 0
0 -20 2 -3 0
0 1 5 9 0
0 2 6 10 0
0 3 7 11 0
0 4 8 12 0
0 13 17 20 0
0 14 18 1 0
0 15 19 2 0
0 16 20 3 0
""")

print("Generated the following WDIMACS test files in the 'test_files' directory:")
for i, filename in enumerate([
    'example1.wcnf', 
    'example2.wcnf', 
    'complex.wcnf', 
    'edge_cases.wcnf',
    'large_indices.wcnf',
    'all_positive.wcnf',
    'all_negative.wcnf',
    'known_patterns.wcnf',
    'realistic.wcnf'
]):
    print(f"{i+1}. {filename}")

print("\nTo test your solution with these files, run:")
print("python3 maxsat_solver.py -question 2 -wdimacs test_files/filename.wcnf -assignment <bitstring>")