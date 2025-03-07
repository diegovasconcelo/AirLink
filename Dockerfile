# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements/ /app/requirements
RUN pip install --upgrade pip
RUN pip install -r requirements/prod.txt

# Copy project
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the sh command to start the app
CMD ["sh", "entrypoint.sh"]