# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Command to run Gunicorn with 4 worker processes and bind it to port 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
