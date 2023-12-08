# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local requirements.txt file to the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade werkzeug
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local code to the container at /app
COPY . /app

# Expose the port that Flask will run on
EXPOSE 5000

# Define the command to run on container start
CMD ["flask", "--app", "/app/server", "run"]
