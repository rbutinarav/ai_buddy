# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install system libraries
RUN apt-get update && apt-get install -y \
    libasound2 libpulse0 \
    && rm -rf /var/lib/apt/lists/*

# Make port 80 available to the world outside this container
EXPOSE 80

# Run your application when the container launches
#CMD ["streamlit", "run", "main.py"]

#bash commands:
#docker build -t ai_buddy_dev .                                       #build docker image
#az login --scope https://management.core.windows.net//.default       #login to azure
#az acr login --name aibuddy                                          #login to azure container registry
#docker tag ai_buddy_dev aibuddy.azurecr.io/ai_buddy_dev:v0.1         #tag docker image
#docker push aibuddy.azurecr.io/ai_buddy_dev:v0.1                     #push docker image to azure container registry
