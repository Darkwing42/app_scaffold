FROM python:3.6

COPY . /usr/src/tasks

WORKDIR /usr/src/tasks

RUN pip install -r requirements.txt

ENTRYPOINT celery -A tasks worker --loglevel=info
