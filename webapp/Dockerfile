FROM python:3.11-slim
COPY . /webapp
WORKDIR /webapp

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN curl -fsSL https://bun.sh/install | bash -s "bun-v0.6.9"

CMD ["reflex", "run"]