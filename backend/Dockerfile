FROM python:3.9.6-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
