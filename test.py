import subprocess

def run_test(question, args, expected_output):
    """
    Runs a test case and checks if the output matches the expected output.
    Args:
        question: The question number (1 or 2).
        args: A list of command-line arguments.
        expected_output: The expected output as a string.
    """
    command = ["./maxsat_solver.py", "-question", str(question)] + args
    print(f"Running test: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if output == expected_output:
            print(f"Test PASSED: Output '{output}' matches expected '{expected_output}'")
        else:
            print(f"Test FAILED: Expected '{expected_output}', got '{output}'")
    except subprocess.CalledProcessError as e:
        print(f"Test FAILED: Program crashed with error:\n{e.stderr}")

def main():
    # Test cases for Exercise 1 (Clause Checking)
    print("=== Testing Exercise 1 (Clause Checking) ===")
    run_test(1, ["-clause", "0.5 2 1 -3 -4 0", "-assignment", "0000"], "1")
    run_test(1, ["-clause", "0.5 2 1 -3 -4 0", "-assignment", "0011"], "0")
    run_test(1, ["-clause", "0.5 2 1 -3 -4 0", "-assignment", "1111"], "1")
    run_test(1, ["-clause", "0.5 2 1 -3 -4 0", "-assignment", "1010"], "1")
    run_test(1, ["-clause", "0.5 2 1 -3 -4 0", "-assignment", "0101"], "1")
    run_test(1, ["-clause", "0.5 2 1 -3 -4 0", "-assignment", "0001"], "1")
    run_test(1, ["-clause", "0.5 2 1 -3 -4 0", "-assignment", "0010"], "0")

    # Test cases for Exercise 2 (WDIMACS Clause Counting)
    print("\n=== Testing Exercise 2 (WDIMACS Clause Counting) ===")
    run_test(2, ["-wdimacs", "example.wcnf", "-assignment", "0000"], "1")
    run_test(2, ["-wdimacs", "example.wcnf", "-assignment", "0001"], "2")
    run_test(2, ["-wdimacs", "example.wcnf", "-assignment", "1111"], "2")
    run_test(2, ["-wdimacs", "example.wcnf", "-assignment", "1010"], "2")
    run_test(2, ["-wdimacs", "example.wcnf", "-assignment", "0101"], "2")

    # Edge cases for Exercise 1
    print("\n=== Testing Edge Cases for Exercise 1 ===")
    run_test(1, ["-clause", "0.5 0", "-assignment", "0000"], "0")  # Empty clause
    run_test(1, ["-clause", "0.5 1 0", "-assignment", "0000"], "0")  # Single positive literal, assignment 0
    run_test(1, ["-clause", "0.5 -1 0", "-assignment", "0000"], "1")  # Single negative literal, assignment 0
    run_test(1, ["-clause", "0.5 1 0", "-assignment", "1000"], "1")  # Single positive literal, assignment 1
    run_test(1, ["-clause", "0.5 -1 0", "-assignment", "1000"], "0")  # Single negative literal, assignment 1

    # Edge cases for Exercise 2
    print("\n=== Testing Edge Cases for Exercise 2 ===")
    run_test(2, ["-wdimacs", "empty.wcnf", "-assignment", "0000"], "0")  # Empty file
    run_test(2, ["-wdimacs", "single_clause.wcnf", "-assignment", "0000"], "1")  # Single clause
    run_test(2, ["-wdimacs", "single_clause.wcnf", "-assignment", "1000"], "1")  # Single clause, assignment 1

    # Invalid inputs
    print("\n=== Testing Invalid Inputs ===")
    run_test(1, ["-clause", "0.5 2 1 -3 -4 0"], "Error: Missing -clause or -assignment argument for question 1.")  # Missing assignment
    run_test(1, ["-assignment", "0000"], "Error: Missing -clause or -assignment argument for question 1.")  # Missing clause
    run_test(2, ["-wdimacs", "example.wcnf"], "Error: Missing -wdimacs or -assignment argument for question 2.")  # Missing assignment
    run_test(2, ["-assignment", "0000"], "Error: Missing -wdimacs or -assignment argument for question 2.")  # Missing WDIMACS file

if __name__ == "__main__":
    main()