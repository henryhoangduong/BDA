set -e

cd "$(dirname "$0")"/..

uv sync

uv run celery -A tasks.parsing_tasks  worker --loglevel=info

uv run fastapi dev main.py 