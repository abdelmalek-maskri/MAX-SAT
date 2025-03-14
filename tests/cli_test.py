#!/usr/bin/env python3
"""
Updated Command-line Test Script for MAXSAT Solver
Adjusted to match your implementation's specific behavior

Usage:
  python3 updated_cli_test.py
"""

import os
import subprocess
import tempfile

# Colors for terminal output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def run_cmd(cmd):
    """Run command and return output"""
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return result.stdout.strip(), result.returncode

def run_test_case(label, cmd, expected):
    """Run a test and check if output matches expected value"""
    print(f"\n{YELLOW}Running:{RESET} {cmd}")
    output, rc = run_cmd(cmd)
    
    if str(output).strip() == str(expected).strip():
        print(f"{GREEN}✓ PASS:{RESET} {label}")
        print(f"  Expected: {expected}")
        print(f"  Received: {output}")
        return True
    else:
        print(f"{RED}✗ FAIL:{RESET} {label}")
        print(f"  Expected: {expected}")
        print(f"  Received: {output}")
        return False

# Create temporary directory for test files
test_dir = tempfile.mkdtemp()

print(f"{YELLOW}=== Testing MAXSAT Solver Command-line Interface ==={RESET}")

# Test Exercise 1: Clause satisfaction
print(f"\n{YELLOW}=== Exercise 1: Clause Satisfaction Tests ==={RESET}")

test_cases_ex1 = [
    # Label, clause, assignment, expected result
    ("Simple positive literal", "0 1 0", "1", "1"),
    ("Simple positive literal (not satisfied)", "0 1 0", "0", "0"),
    ("Simple negative literal", "0 -1 0", "0", "1"),
    ("Simple negative literal (not satisfied)", "0 -1 0", "1", "0"),
    ("Multiple literals", "0 1 2 -3 0", "110", "1"),
    ("Multiple literals (not satisfied)", "0 1 2 -3 0", "001", "0"),
    ("Assignment example 1 from PDF", "0 -1 2 3 0", "000", "1"),
    ("Assignment example 2 from PDF", "0 1 2 3 0", "000", "0"),
    ("Assignment example 3 from PDF", "0 1 2 3 0", "011", "1"),
    ("Example from Exercise 1", "0 2 1 -3 -4 0", "0000", "1"),
    ("Example from Exercise 1 (not satisfied)", "0 2 1 -3 -4 0", "0011", "0")
]

for label, clause, assignment, expected in test_cases_ex1:
    cmd = f"python3 maxsat_solver.py -question 1 -clause \"{clause}\" -assignment {assignment}"
    run_test_case(label, cmd, expected)

# Test Exercise 2: WDIMACS file processing
print(f"\n{YELLOW}=== Exercise 2: WDIMACS File Processing Tests ==={RESET}")

# Create test WDIMACS files
test_files = {
    "example.wcnf": """c Example file
p wcnf 4 2
0 1 2 3 4 0
0 -1 -2 3 -4 0
""",
    "assignment_example.wcnf": """c Example from assignment page 2
p wcnf 3 2
0 -1 2 3 0
0 1 2 3 0
""",
    "complex.wcnf": """c Complex WDIMACS file
p wcnf 5 5
0 1 2 3 0
0 -1 -2 -3 0
0 4 5 -3 0
0 -4 -5 3 0
0 1 -3 5 -2 0
"""
}

for filename, content in test_files.items():
    filepath = os.path.join(test_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)

# Updated expected results to match your implementation
test_cases_ex2 = [
    # Label, wdimacs file, assignment, expected result
    ("Example from documentation 1", os.path.join(test_dir, "example.wcnf"), "0000", "1"),
    ("Example from documentation 2", os.path.join(test_dir, "example.wcnf"), "0001", "2"),
    ("Example from documentation 3", os.path.join(test_dir, "example.wcnf"), "1111", "2"),  # Updated to 2
    ("Assignment example 1", os.path.join(test_dir, "assignment_example.wcnf"), "000", "1"),
    ("Assignment example 2", os.path.join(test_dir, "assignment_example.wcnf"), "011", "2"),
    ("Assignment example 3", os.path.join(test_dir, "assignment_example.wcnf"), "111", "2"),  # Updated to 2
    ("Complex file test 1", os.path.join(test_dir, "complex.wcnf"), "00000", "4"),  # Updated to 4
    ("Complex file test 2", os.path.join(test_dir, "complex.wcnf"), "11111", "4"),  # Updated to 4
    ("Complex file test 3", os.path.join(test_dir, "complex.wcnf"), "10101", "5")   # Updated to 5
]

for label, wdimacs_file, assignment, expected in test_cases_ex2:
    cmd = f"python3 maxsat_solver.py -question 2 -wdimacs {wdimacs_file} -assignment {assignment}"
    run_test_case(label, cmd, expected)

# Clean up
print(f"\n{YELLOW}Cleaning up temporary files...{RESET}")
for filename in test_files:
    os.unlink(os.path.join(test_dir, filename))
os.rmdir(test_dir)

print(f"\n{YELLOW}=== Command-line Testing Complete ==={RESET}")