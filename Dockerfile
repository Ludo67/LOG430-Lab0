# Use an official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy your Python script into the container
COPY HelloWorld.py .

# Set the command to run your script
CMD ["python", "HelloWorld.py"]
