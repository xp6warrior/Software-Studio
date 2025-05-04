FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install pynecone
RUN curl -fsSL https://bun.sh/install | bash -s "bun-v0.6.9"

WORKDIR /webapp
EXPOSE 3000

CMD ["pc", "run"]