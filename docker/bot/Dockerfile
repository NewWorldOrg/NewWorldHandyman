FROM python:3.8.5-alpine

WORKDIR /code

ADD . .

RUN apk add --update-cache --no-cache gcc make musl-dev && \
  pip install pipenv && pipenv install --system

CMD ["python", "main.py"]