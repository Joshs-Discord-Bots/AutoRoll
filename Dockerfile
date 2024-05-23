FROM python:3.12-slim
WORKDIR /app
COPY . .

# Install Poetry
RUN pip install -U poetry

# Install Python dependencies
RUN poetry lock --no-update
RUN poetry install

# Define the entry point for the container
ENTRYPOINT ["poetry", "run", "python", "src/bot.py"]
