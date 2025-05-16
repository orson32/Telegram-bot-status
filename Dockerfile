FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc curl docker.io procps && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY alert_bot.py .

CMD ["sh", "-c", "python bot.py & while true; do python alert_bot.py; sleep 300; done"]
