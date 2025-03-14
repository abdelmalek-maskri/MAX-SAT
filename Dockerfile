# Use the base image provided for the lab
FROM pklehre/ec2025-lab2

# Add your Python script to the Docker image
ADD myprogram /bin/myprogram

# Make the script executable
RUN chmod +x /bin/myprogram

# Set the command to run the test script with your username and submission
CMD ["-username", "axm1962", "-submission", "python3 /bin/myprogram"]