FROM python:2.7-alpine

RUN apk update
RUN apk add --no-cache netcat-openbsd libffi-dev postgresql-dev gcc musl-dev

WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/
RUN chmod +x bootstrap.sh

EXPOSE 8000

CMD ["/bin/sh", "bootstrap.sh"]
