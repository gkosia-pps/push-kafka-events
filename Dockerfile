FROM python:3.7-slim

WORKDIR app

COPY requirements.txt .

COPY . .

RUN pip install virtualenv && \
    virtualenv venv && \
    . venv/bin/activate

RUN pip install -r requirements.txt

CMD ["python", "/app/python_to_kafka.py"]