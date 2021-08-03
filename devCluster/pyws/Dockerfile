FROM ubuntu:latest
USER root:root
RUN mkdir -p /pycode
RUN apt-get update
RUN apt-get install -y python3.9
RUN apt-get install -y pip
COPY . /pycode
RUN pip install kafka-python
#RUN pip install faker

