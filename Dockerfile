FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./app /app

WORKDIR /
CMD ["python", "-m", "app"]


