FROM ubuntu:20.04
MAINTAINER Nathan Grubb "me@nathangrubb.io"

RUN apt-get update -y
RUN apt-get install -y python3-pip

RUN mkdir -p /service
COPY requirements.txt /service
WORKDIR /service
RUN pip3 install -r requirements.txt

COPY . /service
CMD ["python3","-u","."]
