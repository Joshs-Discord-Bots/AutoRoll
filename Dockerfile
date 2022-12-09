# Setup
FROM python:3.10-slim
RUN mkdir /app
WORKDIR /app

# Add Files
COPY ./src .
run pip install --upgrade pip
RUN pip install -r requirements.txt