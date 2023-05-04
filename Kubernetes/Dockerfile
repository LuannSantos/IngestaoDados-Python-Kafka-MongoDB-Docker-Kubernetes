FROM python:3

WORKDIR /usr/src/app

COPY ../python/consumer/. ./

RUN python -m pip install -r ./requirements.txt

CMD ["python", "./kafka_consumer.py"]