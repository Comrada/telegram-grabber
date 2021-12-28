FROM python:3.10-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    python -m pip install --upgrade pip  && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.10-slim as runtime

WORKDIR /app
VOLUME /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
COPY app .
# you must authorize your Telegram application first, then the Telethon will create a session file
COPY server_app.session .

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libpq5 && \
    python -m pip install --upgrade pip && \
    pip install --no-cache /wheels/* && \
    addgroup --system app && adduser --system --group app && \
    chown -R app:app /app

USER app

CMD ["python", "poller.py"]
