# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src/backend/requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the backend directory into the container
COPY ./src/backend /app



# Install Node and NPM
RUN apt-get update && apt-get install -y nodejs npm

# Build the React application
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Set the backend as the working directory
WORKDIR /app/backend

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME AzureVM-PricingHelper

# Run app.py when the container launches
CMD ["python", "app.py"]
