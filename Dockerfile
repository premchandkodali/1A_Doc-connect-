# Use official Python image with explicit AMD64 platform
FROM --platform=linux/amd64 python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Default command to run your main script
CMD ["python", "main.py"]
