FROM python:3.10-slim

WORKDIR /webapp

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    gcc \
    build-essential \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://bun.sh/install | bash -s "bun-v0.6.9"

COPY webapp/requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY mail/requirements.txt webapp/mail/requirements.txt
RUN pip install --no-cache-dir -r webapp/mail/requirements.txt

COPY webapp .
COPY database/models ./webapp/models2
COPY mail/src webapp/mail

CMD ["reflex", "run"]