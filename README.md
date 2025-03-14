# MAXSAT Lab - Testing and Submission Guide

This guide will help you test your implementation of the MAXSAT problem and prepare it for submission.

## Files in this Project

- `maxsat_solver.py` - Contains implementations for Exercises 1 and 2
- `exo3.py` - Contains the evolutionary algorithm implementation for Exercise 3
- `test_script.py` - A simple script to test your implementation
- `Dockerfile` - For creating a Docker container to test and submit your solution

## Testing Your Implementation Locally

1. Make sure you have Python installed on your system.

2. Run the test script to verify your implementation:
   ```
   python test_script.py
   ```

3. Check the output to ensure that all tests pass.

## Preparing for Docker Submission

1. Make sure you have Docker installed on your system.

2. Update the Dockerfile with your username (replace `YOUR_USERNAME` with your actual username).

3. Create a directory structure as specified in the lab document:
   ```
   mkdir -p ec2025cw2-YOUR_USERNAME
   cp maxsat_solver.py exo3.py Dockerfile ec2025cw2-YOUR_USERNAME/
   ```

4. Create or add your PDF file for Exercises 4 and 5 to the directory:
   ```
   cp YOUR_PDF_FILE.pdf ec2025cw2-YOUR_USERNAME/exercise.pdf
   ```

## Building and Testing the Docker Image

1. Build the Docker image:
   ```
   docker build ec2025cw2-YOUR_USERNAME -t ec2025cw2-YOUR_USERNAME
   ```

2. Test the Docker image:
   ```
   docker run --platform=linux/amd64 ec2025cw2-YOUR_USERNAME
   ```

## Creating the Submission Zip File

1. Create a zip file of the directory:
   ```
   zip -r ec2025cw2-YOUR_USERNAME.zip ec2025cw2-YOUR_USERNAME
   ```

2. Submit the zip file on Canvas.

## Troubleshooting

- If you encounter issues with the Docker build or run commands, check the lab document for additional guidance.
- Make sure all file paths are correct and that you've replaced `YOUR_USERNAME` with your actual username.
- Verify that your code returns the expected outputs for the test cases.
- If your code requires additional Python packages, add them to the Dockerfile using `RUN apt-get -y install <package-name>`.