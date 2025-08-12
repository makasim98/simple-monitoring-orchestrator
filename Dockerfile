# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install uv globally
RUN pip install uv

# Set the working directory in the container
WORKDIR /app

# Copy pyproject.toml and agent directory
COPY pyproject.toml .
COPY ./agent /app

# Install dependencies using uv from the pyproject.toml file
RUN uv sync

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set an environment variable for Flask to run the app
ENV FLASK_APP=app.py

# Define the command to run the application using python -m flask
CMD ["uv", "run", "app.py"]