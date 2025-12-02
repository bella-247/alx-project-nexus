FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (cache optimization)
COPY requirements.lock .

RUN pip install --no-cache-dir -r requirements.lock

# Copy project code
COPY . .

# Ensure SQLite directory exists
RUN mkdir -p /data

# Command to run the server
CMD ["gunicorn", "polls_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
