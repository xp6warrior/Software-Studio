FROM python:3.11-slim
COPY . /rte
#COPY ../database/models /rte/models
WORKDIR /rte

RUN pip install --no-cache-dir -r requirements.txt

#run scheduler by default
CMD ["python", "scheduler.py"]
