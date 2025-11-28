#!/usr/bin/env bash
set -euo pipefail
# build.sh - helper to set up, run and test the Online Poll System backend
# Usage: ./build.sh [up|local|migrate|test|run|down|help]

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$ROOT_DIR/.env"

usage(){
  cat <<EOF
Usage: $0 <command>

Commands:
  up       - Start services with Docker Compose (builds images)
  down     - Stop and remove containers and volumes
  local    - Set up a local Python virtualenv, install deps and run migrations
  migrate  - Run Django migrations (uses .venv if present)
  test     - Run Django tests (uses .venv if present)
  run      - Run Django development server locally (uses .venv if present)
  help     - Show this help

Examples:
  ./build.sh up        # start postgres, redis, and the web container
  ./build.sh local     # prepare .venv and install dependencies for local dev
  ./build.sh test      # run test suite (after local setup)

Note: Make this script executable with: chmod +x build.sh
EOF
}

ensure_env(){
  if [ ! -f "$ENV_FILE" ] && [ -f "$ROOT_DIR/.env.example" ]; then
    echo "Creating .env from .env.example"
    cp "$ROOT_DIR/.env.example" "$ENV_FILE"
  fi
}

check_cmd(){
  command -v "$1" >/dev/null 2>&1
}

docker_up(){
  ensure_env
  if check_cmd docker && check_cmd docker-compose; then
    echo "Starting services with docker compose..."
    docker compose up --build -d
    echo "Services started. Swagger UI: http://localhost:8000/api/docs/"
  else
    echo "Docker or docker-compose not available. Install Docker and Docker Compose to use this mode."
    exit 1
  fi
}

docker_down(){
  if check_cmd docker && check_cmd docker-compose; then
    echo "Stopping and removing containers..."
    docker compose down -v
  else
    echo "Docker not available. Skipping."
  fi
}

local_setup(){
  if ! check_cmd python3; then
    echo "python3 not found. Install Python 3.8+ and try again."
    exit 1
  fi

  if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv"
    python3 -m venv .venv || { echo "Failed to create venv. On Debian/Ubuntu install python3-venv."; exit 1; }
  fi

  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  python manage.py migrate
  echo "Local setup complete. Run './build.sh run' to start the dev server."
}

migrate_cmd(){
  if [ -f .venv/bin/activate ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
  fi
  python manage.py migrate
}

test_cmd(){
  if [ -f .venv/bin/activate ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
  fi
  python manage.py test --verbosity=2
}

run_cmd(){
  if [ -f .venv/bin/activate ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
  fi
  python manage.py runserver 0.0.0.0:8000
}

case "${1:-help}" in
  up)
    docker_up
    ;;
  down)
    docker_down
    ;;
  local)
    local_setup
    ;;
  migrate)
    migrate_cmd
    ;;
  test)
    test_cmd
    ;;
  run)
    run_cmd
    ;;
  help|*)
    usage
    ;;
esac
