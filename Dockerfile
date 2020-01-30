FROM ubuntu:16.04

WORKDIR /home/brozzler

# Install suitable version of Python:
RUN apt-get update
RUN apt-get install -y python3-dev python3-gdbm curl git libffi-dev libssl-dev
RUN curl "https://bootstrap.pypa.io/get-pip.py" | python3.5

RUN apt-get -y install gcc

RUN apt-get install -y dbus

RUN useradd -ms /bin/bash brozzler

COPY . .

RUN python3.5 setup.py install

EXPOSE 5001

USER brozzler

CMD bc-launch-ui --host 0.0.0.0