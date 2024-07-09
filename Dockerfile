# Use an official Python runtime as a parent image
FROM   python

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY server.py  /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app 

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -r /app/requirements.txt

EXPOSE 5050
# Define environment variable
#ENV TEMP 

# Run app.py when the container launches
CMD ["python3", "server.py"]

