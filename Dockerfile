# Use the base image 

FROM pklehre/ec2025-lab2

# Add the Python script to the Docker image

ADD axm1962.py /bin

# to make the script executable:
# RUN chmod +x /bin/axm1962.py

# Set the command to run the test script with your username and submission


CMD ["-username", "axm1962", "-submission", "python3 /bin/axm1962.py"]
