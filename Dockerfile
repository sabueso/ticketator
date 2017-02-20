FROM python:2.7

RUN apt-get update
RUN apt-get install -Vy netcat
RUN apt-get install -Vy libffi-dev

WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/
RUN chmod +x bootstrap.sh

EXPOSE 8000

CMD ["/bin/bash", "bootstrap.sh"]
