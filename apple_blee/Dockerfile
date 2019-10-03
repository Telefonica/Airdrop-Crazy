FROM ubuntu:bionic

MAINTAINER Lucas Fernandez

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip


RUN mkdir -p /usr/src/app

# Update working directory
WORKDIR /usr/src/app

# copy everything from this directory to server/flask docker container
COPY . /usr/src/app/

RUN chmod +x ./install.sh

RUN bash ./install.sh

# Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get install -y --reinstall wireless-tools

CMD [ "/bin/bash" ]