FROM python:3.14

WORKDIR /code

RUN pip install poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]