FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
# Ensure build and run scripts are executable and run the build step
RUN chmod +x /app/build.sh /app/run.sh || true
RUN /bin/bash -lc "./build.sh"
CMD ["/bin/bash", "-lc", "./run.sh"]
