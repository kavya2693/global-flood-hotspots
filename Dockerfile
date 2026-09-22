FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt tabulate

COPY src ./src
COPY data ./data
COPY tests ./tests

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "floodhotspots", "run"]
