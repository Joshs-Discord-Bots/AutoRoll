# Setup
FROM python:3.9
WORKDIR /autoroll-app

# Add Files
ADD compose.yaml .
COPY requirements.txt .
COPY bot.py .
COPY cogs ./cogs

RUN pip install -r requirements.txt

# Start Application
CMD ["python", "./bot.py"]