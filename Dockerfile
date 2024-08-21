# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the relevant directories
COPY app/main.py /app/
COPY requirements.txt /app/
COPY app/config.py /app/
COPY app/crud.py /app/
COPY app/ia.py /app/
COPY app/routes.py /app/
COPY app/wordcloudMod.py /app/

# Install any needed packages specified in requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

RUN mkdir -p /app/files/ia /app/files/wordcloud

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application, specifying the module as app.main
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
