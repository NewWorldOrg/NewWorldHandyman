FROM python:3.8.5-alpine

WORKDIR /code

ADD . .

RUN apk add --update-cache --no-cache linux-headers g++ make && \
  pip install pipenv && pipenv install --system

CMD ["python", "main.py"]
