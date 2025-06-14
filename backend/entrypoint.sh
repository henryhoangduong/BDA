#!/bin/sh
# start FastAPI in background
/app/.venv/bin/fastapi run /app/main.py --port 8080 &

/app/.venv/bin/celery \
  -A core.celery_config.celery_app worker \
  --loglevel=info -Q parsing