FROM python:3.12

WORKDIR /app
RUN pip install gunicorn==20.1.0
# Устанавливаем зависимости для PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
# Устанавливаем psycopg2 или psycopg
RUN pip install psycopg2-binary

COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
