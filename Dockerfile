FROM python:3.9

WORKDIR /app

RUN pip3 install discord.py

CMD ["python3", "bot.py"]