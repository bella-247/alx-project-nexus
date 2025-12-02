FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies (use requirements.txt or requirements.lock if you prefer)
COPY requirements.lock requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.lock || pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . /app

# Ensure helper scripts are executable and create data directory for sqlite
RUN chmod +x /app/build.sh /app/run.sh || true
RUN mkdir -p /data

# Run build step (install static assets). Do NOT run migrations here — they run at container start.
RUN /bin/bash -lc "./build.sh"

# Start the app via run.sh which runs migrations then gunicorn and respects $PORT
CMD ["/bin/bash", "-lc", "./run.sh"]
