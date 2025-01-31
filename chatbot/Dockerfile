# Use Python slim image as the base
FROM python:3.11-slim

# Set working directory
WORKDIR /chatbot

# Copy requirements first to leverage Docker cache
COPY ./requirements.txt .

# Install system dependencies for psycopg2-binary
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*


# Install dependencies
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose port if needed (adjust as necessary)
EXPOSE 8000


