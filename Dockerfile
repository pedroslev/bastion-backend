# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the relevant directories
COPY app/ .
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

RUN mkdir -p /app/files/ia /app/files/wordcloud

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application, specifying the module as app.main
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
