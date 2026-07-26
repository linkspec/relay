FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY api/ api/
COPY models/ models/
COPY services/ services/
COPY tools/ tools/
COPY certs/ certs/

COPY app.py .
COPY config.py .

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "1", "--capture-output", "--log-level", "info", "-b", "0.0.0.0:8000", "app:app"]