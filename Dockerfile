# Use an official Python runtime as a parent image
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY prod_requirements.txt ./
COPY setup.py ./
COPY ./app ./app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r prod_requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable
ENV NAME PixzinhoBot

# Run app.py when the container launches
CMD ["python", "setup.py"]
