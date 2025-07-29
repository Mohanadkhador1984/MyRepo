FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", "quiz_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info"]
