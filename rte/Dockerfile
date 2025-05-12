FROM python:3.11-slim

WORKDIR /rte

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#run scheduler by default
CMD ["python", "scheduler.py"]
