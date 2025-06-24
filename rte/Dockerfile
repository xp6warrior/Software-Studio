FROM python:3.11-slim

WORKDIR /rte

COPY rte/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY mail/requirements.txt src/mail/requirements.txt
RUN pip install --no-cache-dir -r src/mail/requirements.txt

COPY rte .
COPY database/models src/models
COPY mail/src src/mail

WORKDIR /rte/src

#run scheduler by default
CMD ["python", "./scheduler.py"]
