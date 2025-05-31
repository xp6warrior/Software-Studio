FROM python:3.11-slim

WORKDIR /webapp

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://bun.sh/install | bash -s "bun-v0.6.9"

COPY webapp/requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY webapp .
COPY database/models ./webapp/models2

CMD ["reflex", "run"]