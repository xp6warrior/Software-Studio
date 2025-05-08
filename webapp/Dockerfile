FROM python:3.11-slim
WORKDIR /webapp
COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN curl -fsSL https://bun.sh/install | bash -s "bun-v0.6.9"

CMD ["reflex", "run"]