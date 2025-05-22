FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
