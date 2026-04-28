FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml /app/pyproject.toml

RUN uv sync --frozen --no-dev || uv sync --no-dev

COPY app /app/app

EXPOSE 3000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]

