FROM ubuntu:14.04

# backup old sources.list
#RUN mv /etc/apt/sources.list /etc/apt/sources.list.bk

#ADD sources.list /etc/apt/sources.list

RUN apt-get -qqy update && apt-get install -y \
    curl \
    python3 \
    python3-dev \
    python3-pip \
    gunicorn


# for copy requirements.txt to container
COPY . /server/docker-compose

WORKDIR /server

RUN pip3 install -r docker-compose/requirements.txt

#WORKDIR /server
